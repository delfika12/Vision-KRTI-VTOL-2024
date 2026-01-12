import argparse
import os
import platform
import sys
import time  # Tambahkan impor untuk penghitungan waktu
from pathlib import Path
import torch
import cv2
from models.common import DetectMultiBackend
from utils.general import (
    LOGGER,
    check_img_size,
    check_imshow,
    non_max_suppression,
    scale_boxes,
)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device, smart_inference_mode

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# ROS1 Imports
import rospy
from std_msgs.msg import String

@smart_inference_mode()
def run(
    weights=ROOT / "best-KRTI.pt",  # model path
    source="0",  # webcam source
    imgsz=(640, 640),  # inference size (height, width)
    conf_thres=0.25,  # confidence threshold
    iou_thres=0.45,  # NMS IOU threshold
    max_det=10,  # maximum detections per image
    device="",  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    line_thickness=3,  # bounding box thickness (pixels)
    hide_labels=False,  # hide labels
    hide_conf=False,  # hide confidences
    half=False,  # use FP16 half-precision inference
):
    source = str(source)
    save_img = False
    webcam = source.isnumeric()

    # Initialize ROS Node and Publisher
    rospy.init_node('singlecam_node', anonymous=True)
    pub = rospy.Publisher('singlecam', String, queue_size=10)

    # Pilih device
    device = select_device(device)
    
    # Patch: Ganti PosixPath ke WindowsPath jika dijalankan di Windows
    if platform.system() == "Windows":
        import pathlib
        pathlib.PosixPath = pathlib.WindowsPath

    # Load model
    model = DetectMultiBackend(weights, device=device, dnn=False, data=None, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # periksa ukuran gambar

    # Inisialisasi webcam
    cap = cv2.VideoCapture(int(source))
    assert cap.isOpened(), f"Failed to open {source}"

    # Lakukan pemanasan model
    model.warmup(imgsz=(1 if pt or model.triton else 1, 3, *imgsz))
    seen = 0

    def get_grid_position(x, y, width, height):
        """Determine the grid position (1-9) based on the coordinates."""
        step_x = width // 3
        step_y = height // 3
        col = x // step_x
        row = y // step_y
        return int(row * 3 + col + 1)

    def draw_grid(frame):
        """Draw grid lines on the frame."""
        height, width, _ = frame.shape
        step_x = width // 3
        step_y = height // 3
        # Draw vertical lines
        for i in range(1, 3):
            cv2.line(frame, (i * step_x, 0), (i * step_x, height), (255, 255, 255), 1)
        # Draw horizontal lines
        for i in range(1, 3):
            cv2.line(frame, (0, i * step_y), (width, i * step_y), (255, 255, 255), 1)
        return frame

    grid_positions = {
        1: "Top Left", 2: "Top Center", 3: "Top Right",
        4: "Middle Left", 5: "Center", 6: "Middle Right",
        7: "Bottom Left", 8: "Bottom Center", 9: "Bottom Right"
    }

    while True:
        ret, im0 = cap.read()
        if not ret:
            LOGGER.warning(f"Failed to grab frame from {source}")
            break
        
        start_time = time.time()  # Mulai penghitungan waktu di sini

        # Konversi gambar dari BGR ke RGB dan ubah bentuk tensor
        im = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 ke fp16/32
        im /= 255.0  # Normalisasi ke rentang 0.0 - 1.0
        im = im.permute(2, 0, 1).unsqueeze(0)  # Ubah bentuk menjadi (1, 3, tinggi, lebar)

        # Inference
        pred = model(im)

        # Non-Maximum Suppression (NMS)
        pred = non_max_suppression(pred, conf_thres, iou_thres, max_det=max_det)

        # Proses hasil deteksi
        for i, det in enumerate(pred):  # per image
            seen += 1
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Ubah skala bounding box dari ukuran model ke ukuran asli gambar
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Tambahkan kotak dan label
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = None if hide_labels else (names[c] if hide_conf else f"{names[c]} {conf:.2f}")
                    annotator.box_label(xyxy, label, color=colors(c, True))

            # Tampilkan hasil deteksi
            im0 = annotator.result()
            im0 = draw_grid(im0)  # Draw grid lines

            if len(det):
                # Get the last detection (highest confidence/last in list) or iterate if needed
                # For simplicity in display, we show the position of the last processed object
                # or we can modify the loop to print for all. 
                # Let's just use the last one for the main "Position" text or add it to the label?
                # The user asked to show "di posisi mana objek ditemukan".
                
                # We already iterated above. Let's find the position for the last one or all.
                # Re-calculating center for the last detection to show in large text
                for *xyxy, conf, cls in reversed(det):
                    x_center = (xyxy[0] + xyxy[2]) / 2
                    y_center = (xyxy[1] + xyxy[3]) / 2
                    grid_pos = get_grid_position(x_center, y_center, im0.shape[1], im0.shape[0])
                    pos_text = grid_positions.get(grid_pos, "Unknown")
                    
                    # Display position text on top of the object or globally
                    # Global display at the bottom left
                    cv2.putText(im0, f"Pos: {pos_text}", (10, im0.shape[0] - 40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    # Log to console
                    log_msg = f"Detected {names[int(cls)]} at {pos_text}"
                    print(log_msg)

                    # Publish to ROS
                    # Format: "ObjectClass,Position"
                    ros_msg = f"{names[int(cls)]},{pos_text}"
                    pub.publish(ros_msg)
                    
                    break # Just show for one to avoid text overlap clutter if multiple objects
            elapsed_time = time.time() - start_time  # Hitung waktu yang dibutuhkan
            fps = 1 / elapsed_time if elapsed_time > 0 else 0  # Hitung FPS
            
            # Tampilkan FPS di pojok kanan bawah
            cv2.putText(im0, f'FPS: {fps:.0f}', (im0.shape[1] - 120, im0.shape[0] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.imshow("YOLOv5 Detection", im0)
            if cv2.waitKey(1) == ord("q"):  # tekan 'q' untuk keluar
                break

    cap.release()
    cv2.destroyAllWindows()

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", nargs="+", type=str, default=ROOT / "best-KRTI.pt", help="model path")
    parser.add_argument("--source", type=str, default="0", help="webcam source (default is 0)")
    parser.add_argument("--imgsz", "--img", "--img-size", nargs="+", type=int, default=[640], help="inference size h,w")
    parser.add_argument("--conf-thres", type=float, default=0.50, help="confidence threshold")
    parser.add_argument("--iou-thres", type=float, default=0.45, help="NMS IoU threshold")
    parser.add_argument("--max-det", type=int, default=10, help="maximum detections per image")
    parser.add_argument("--device", default="", help="cuda device, i.e. 0 or 0,1,2,3 or cpu")
    parser.add_argument("--line-thickness", default=3, type=int, help="bounding box thickness (pixels)")
    parser.add_argument("--hide-labels", default=False, action="store_true", help="hide labels")
    parser.add_argument("--hide-conf", default=False, action="store_true", help="hide confidences")
    parser.add_argument("--half", action="store_true", help="use FP16 half-precision inference")
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand ukuran gambar jika hanya satu nilai diberikan
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)