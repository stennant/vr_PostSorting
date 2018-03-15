'''
This class has the setters and getters for the parameters. The parameters need to be set in main
and they can be called by calling the getter functions.
For example to set and get filepath:
prm.set_filepath('C:/Users/s1466507/Documents/Ephys/deep MEC/day3/2016-08-29_09-15-54/')
prm.get_filepath()
'''


class Parameters:

    is_vr = True
    is_open_field = False

    filepath = ''
    filename = ''
    date = ''
    file = ''
    behaviour_path = ''
    behaviour_analysis_path = ''
    behaviour_data_path = ''
    mountain_sort_path = ''
    firings_path = ''
    spike_path = ''
    continuous_path = ''
    fft_path = ''
    ephys_path = ''
    ephys_data_path = ''
    ephys_analysis_path = ''
    spike_path = ''
    klustakwik_path = ''
    klustakwik_analysis_path = ''

    sampling_rate = 30000
    num_channels = 0
    current_tetrode = 0
    current_continuous = 0
    num_tetrodes = 0
    good_channels = []
    TRACK_LENGTH = 0
    STOP_THRESHOLD = 0.7
    outbound = 0
    reward_zone = 0
    movement_ch = '100_ADC2.continuous'
    opto_ch = '100_ADC3.continuous'
    first_trial_channel = '100_ADC4.continuous'
    second_trial_channel = '100_ADC5.continuous'
    spike_threshold = 120  # uV
    waveform_size = 40
    recording_size = 0
    tetrode = 0


    opto_tagging_done = False


    def __init__(self):
        return

    def get_is_vr(self):
        return Parameters.is_vr

    def set_is_vr(self, is_vr):
        Parameters.is_vr = is_vr

    def get_is_open_field(self):
        return Parameters.is_open_field

    def set_is_open_field(self, is_open_field):
        Parameters.is_open_field = is_open_field

    def get_date(self):
        return Parameters.date

    def set_date(self, dt):
        Parameters.date = dt

    def get_filepath(self):
        return Parameters.filepath

    def set_filepath(self, fp):
        Parameters.filepath = fp

    def get_filename(self):
        return self.filename

    def set_filename(self, fn):
        Parameters.filename = fn

    def get_behaviour_path(self):
        return self.behaviour_path

    def set_behaviour_path(self, fn):
        Parameters.behaviour_path = fn

    def get_behaviour_data_path(self):
        return self.behaviour_data_path

    def set_behaviour_data_path(self, fn):
        Parameters.behaviour_data_path = fn

    def get_behaviour_analysis_path(self):
        return self.behaviour_analysis_path

    def set_behaviour_analysis_path(self, fn):
        Parameters.behaviour_analysis_path = fn

    def get_firings_path(self):
        return self.firings_path

    def set_firings_path(self, fn):
        Parameters.firings_path = fn

    def get_ephys_path(self):
        return self.ephys_path

    def set_ephys_path(self, fn):
        Parameters.ephys_path = fn

    def get_spike_path(self):
        return self.spike_path

    def set_spike_path(self, sp):
        Parameters.spike_path = sp

    def get_continuous_path(self):
        return self.continuous_path

    def set_continuous_path(self, co):
        Parameters.continuous_path = co

    def get_fft_path(self):
        return self.fft_path

    def set_fft_path(self, ff):
        Parameters.fft_path = ff

    def get_ephys_data_path(self):
        return self.ephys_data_path

    def set_ephys_data_path(self, ed):
        Parameters.ephys_data_path = ed


    def get_ephys_analysis_path(self):
        return self.ephys_analysis_path

    def set_ephys_analysis_path(self, ed):
        Parameters.ephys_analysis_path = ed

    def get_mountain_sort_path(self):
        return self.mountain_sort_path

    def set_mountain_sort_path(self, ms):
        Parameters.mountain_sort_path = ms



    def get_klustakwik_path(self):
        return self.klustakwik_path

    def set_klustakwik_path(self, kk):
        Parameters.klustakwik_path = kk

    def get_klustakwik_analysis_path(self):
        return self.klustakwik_analysis_path

    def set_klustakwik_analysis_path(self, kka):
        Parameters.klustakwik_analysis_path = kka

    def get_file(self):
        return self.file

    def set_file(self, fp, fn):
        Parameters.filepath + Parameters.filename + ".raw.kwd"

    def get_num_channels(self):
        return self.num_channels

    def set_num_channels(self, n_ch):
        Parameters.num_channels = n_ch

    def get_num_tetrodes(self):
        return self.num_tetrodes

    def set_num_tetrodes(self, n_tet):
        Parameters.num_tetrodes = n_tet

    def get_current_tetrode(self):
        return self.current_tetrode

    def set_current_tetrode(self, curr_tet):
        Parameters.current_tetrode = curr_tet

    def get_current_continuous(self):
        return self.current_continuous

    def set_current_continuous(self, curr_con):
        Parameters.current_continuous = curr_con

    def get_good_channels(self):
        return self.good_channels

    def set_good_channels(self, channels):
        Parameters.good_channels = channels

    def get_track_length(self):
        return self.TRACK_LENGTH

    def set_track_length(self, tr_length):
        Parameters.TRACK_LENGTH = tr_length

    def get_beginning_of_outbound(self):
        return self.outbound

    def set_beginning_of_outbound(self, outbound):
        Parameters.outbound = outbound

    def get_reward_zone(self):
        return self.reward_zone

    def set_reward_zone(self, reward_zone):
        Parameters.reward_zone = reward_zone

    def get_stop_threshold(self):
        return self.STOP_THRESHOLD

    def set_stop_threshold(self, stop_thr):
        Parameters.STOP_THRESHOLD = stop_thr

    def get_movement_ch(self):
        return self.movement_ch

    def set_movement_ch(self, movement_ch):
        Parameters.movement_ch = movement_ch

    def get_opto_ch(self):
        return self.opto_ch

    def set_opto_ch(self, opto_ch):
        Parameters.opto_ch = opto_ch

    def get_first_trial_channel(self):
        return self.first_trial_channel

    def set_first_trial_channel(self, f_chan):
        Parameters.first_trial_channel = f_chan

    def get_second_trial_channel(self):
        return self.second_trial_channel

    def set_second_trial_channel(self, s_chan):
        Parameters.second_trial_channel = s_chan

    def get_spike_detection_threshold(self):
        return self.spike_threshold

    def set_spike_detection_threshold(self, spike_threshold):
        Parameters.spike_threshold = spike_threshold


    def get_waveform_size(self):
        return self.waveform_size


    def set_waveform_size(self, waveform_size):
        Parameters.waveform_size = waveform_size


    def get_recording_size(self):
        return self.recording_size


    def set_recording_size(self, recording_size):
        Parameters.recording_size = recording_size

    def set_tetrode(self, tet):
        Parameters.tetrode = tet

    def get_tetrode(self):
        return self.tetrode

    def set_sampling_rate(self, sr):
        Parameters.sampling_rate = sr

    def get_sampling_rate(self):
        return self.sampling_rate

    def set_opto_tagging_done(self, ot):
        Parameters.opto_tagging_done = ot

    def get_opto_tagging_done(self):
        return self.opto_tagging_done
