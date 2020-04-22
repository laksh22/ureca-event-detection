import argparse
from train import Trainer
from test import Tester


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode", help="Pass either 'train' or 'test'")
    parser.add_argument(
        "video", help="Path to the video file")
    parser.add_argument(
        "data", help="Path where training data is stored or should be stored")
    parser.add_argument(
        "tracks", help="Path where tracking data is stored or should be stored")
    parser.add_argument(
        "--anomalies", help="Path where anomaly data should be stored after testing")
    args = parser.parse_args()

    if(args.mode == "train"):
        trainer = Trainer(args.video, args.data, args.tracks)
        trainer.train()
    else:
        tester = Tester(args.video, args.data,
                        tracks_path=args.tracks, anomalies_path=args.anomalies)
        tester.test()
