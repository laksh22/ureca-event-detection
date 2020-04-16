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
        "--tracks", help="Path where tracking data is stored (if any)")
    args = parser.parse_args()

    if(args.mode == "train"):
        trainer = Trainer(args.video, args.data, args.tracks)
        trainer.train()
    else:
        tester = Tester(args.video, args.data, args.tracks)
        tester.test()
