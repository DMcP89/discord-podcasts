import wave
import discord


class BufSink(discord.reader.AudioSink):
    def __init__(self):
        self.bytearr_buf = bytearray()
        self.sample_width = 2
        self.sample_rate = 96000
        self.bytes_ps = 192000


    def write(self, data):
        self.bytearr_buf += data.data

    def freshen(self, idx):
        self.bytearr_buf = self.bytearr_buf[idx:]

def poster(bot, buffer, target_channel):
    global close_flag
    # we don't want the thread to end, so just loop forever
    while True:
        if close_flag:
            # if the slice isn't all 0s, create an AudioData instance with it,
            # needed by the speech_recognition lib
            if len(buffer.bytearr_buf) > 960000:
                data = buffer.bytearr_buf
                # if the slice isn't all 0s, create an AudioData instance with it,
                # needed by the speech_recognition lib
                if any(data):
                    # trim leading zeroes, should be more accurate
                    idx_strip = data.index(next(filter(lambda x: x!=0, data)))
                    if idx_strip:
                        buffer.freshen(idx_strip)
                        data = buffer.bytearr_buf
                    wavef = wave.open('sound.wav','w')
                    wavef.setnchannels(1) # stereo
                    wavef.setsampwidth(buffer.sample_width) 
                    wavef.setframerate(buffer.sample_rate)
                    wavef.writeframesraw(bytes(buffer.bytearr_buf))
            break