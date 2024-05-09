from aiortc import MediaStreamTrack
from av import VideoFrame

from core.augmented_reality import find_and_warp


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """
    kind = "video"

    def __init__(self, track, v_player):
        super().__init__()  # don't forget this!
        self.track = track
        self.video_player = v_player
        self.cached_ref_pts = None

    async def recv(self):
        frame = await self.track.recv()

        source = self.video_player.source()
        if source is None:
            return frame

        warped, self.cached_ref_pts = find_and_warp(frame.to_ndarray(format="bgr24"), source)
        if warped is None:
            return frame

        new_frame = VideoFrame.from_ndarray(warped, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base

        return new_frame
