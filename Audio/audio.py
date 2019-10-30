import numpy as np
import pyaudio
import time
from scipy import signal
# import matplotlib.animation as anm
import matplotlib.pyplot as plt

class AudioFilter:
    def __init__(self):
        # オーディオに関する設定
        self.p = pyaudio.PyAudio()
        self.channels = 1 # マイクがモノラルの場合は1にしないといけない
        self.rate = 16000 #48000 # DVDレベルなので重かったら16000にする
        self.CHUNK = 2**11
        self.format = pyaudio.paInt16
        self.stream = self.p.open(
                        format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        frames_per_buffer=self.CHUNK,
                        output=True,
                        input=True,
                        stream_callback=self.callback,
                        input_device_index=4)
        self.ndarray = np.array([])
        self.alldata = np.array([])
        self.cnt=-1

        self.fpass = 1.0 * 10**2              # 通過遮断周波数[Hz]
        self.fstop = 1.0 * 10**3              # 阻止域遮断周波数[Hz]
        self.gpass = 0.4                      # 通過域最大損失量[dB]
        self.gstop = 30                       # 阻止域最小減衰量[dB]

        #正規化
        self.fn = self.rate/2
        self.wp = self.fpass/self.fn
        self.ws = self.fstop/self.fn
        #フィルタの係数設計（バタワースフィルタ）
        self.N, self.Wn = signal.buttord(self.wp, self.ws, self.gpass, self.gstop)  #オーダーとバターワースの正規化周波数を計算
        self.b, self.a = signal.butter(self.N, self.Wn, "highpass")            #フィルタ伝達関数の分子と分母を計算

    # コールバック関数（再生が必要なときに呼び出される）
    def callback(self, in_data, frame_count, time_info, status):
        # out_data = in_data
        self.ndarray = np.frombuffer(in_data, dtype='int16')
        self.alldata = np.append(self.alldata,self.ndarray)
        self.y = signal.filtfilt(self.b, self.a, self.ndarray)                  #信号に対してフィルタをかける
        self.y = self.y.astype(dtype='int16')
        self.cnt=self.cnt+self.CHUNK
        out_data = self.y
        return (out_data, pyaudio.paContinue)


    def close(self):
        self.p.terminate()

class Monitor:
    def __init__(self):
        self.ylim = .02
        self.plot_num1=16000;
        self.wave_x1 = 0
        self.wave_y1 = 0
        self.data1 = np.array([])

    def graphplot(self):
        self.wave_x1 = range(0, self.plot_num1)
        self.wave_y1 = self.data1/327680.0

        plt.clf()
        plt.plot(self.wave_x1, self.wave_y1)
        plt.axis([0, self.plot_num1, -self.ylim, self.ylim])
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")

        plt.pause(.01)

if __name__ == "__main__":
    # AudioFilterのインスタンスを作る場所

    af = AudioFilter()
    moni = Monitor()

    # ストリーミングを始める場所
    af.stream.start_stream()

    # ノンブロッキングなので好きなことをしていていい場所
    while af.stream.is_active():#and af2.stream.is_active():
        try:
            time.sleep(0.03)

            if  af.cnt>moni.plot_num1 :
                moni.data1=af.alldata[af.cnt-moni.plot_num1:af.cnt:]
                moni.graphplot()

        except KeyboardInterrupt:
            break

    print("save...")
    f = open('data.txt', 'w')
    f.write('%data[]\n')
    for i in af.alldata:
        f.write(str(i))
        f.write('\n')
    f.close()
    print("done")

    # ストリーミングを止める場所
    af.stream.stop_stream()
    af.stream.close()
    af.close()
