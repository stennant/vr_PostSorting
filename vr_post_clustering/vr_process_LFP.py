import glob
import os
import vr_parameters
import vr_process_movement
import vr_plot_stops
import vr_plot_spikes
import vr_stops
import vr_sorted_firing_times
import vr_trial_types
import vr_plot_continuous_data
import vr_fft
import vr_filter
import vr_oscillations
import vr_rewrite_continuous_data
import vr_optogenetics
import vr_optogenetics_behaviour
#import vr_theta_gamma_correlation
import vr_referencing
import numpy as np
import vr_split_data
import vr_spectrogram
import vr_track_location_analysis
import vr_track_location_plots
import vr_power_calculations


def process_movement_and_stationary(prm, data, channel):
    #split based on stops
    before_stop, after_stop = vr_track_location_analysis.find_before_and_after_stops(prm,data[1000000:75000000,:])
    #vr_track_location_plots.make_stop_start_continuous_plot(prm, channel, before_stop, after_stop)
    vr_track_location_analysis.stop_start_power_spectra(prm, before_stop, after_stop, channel) # FIGURE 1 B : EXAMPLE POWER SPECTRA OF STOP/START
    vr_power_calculations.calculate_and_plot_pooled_gamma_power_stop_start(prm, before_stop, after_stop,  channel)# FIGURE 1 C : POOLED POWER CALCULATIONS OF STOP/START

    return before_stop, after_stop


def process_movement_and_stationary_locations(prm,before_stop, after_stop, channel):
    #before/after power spectra at different locations
    #split based on location
    before_stop_outbound, before_stop_rewardzone, before_stop_homebound = vr_track_location_analysis.split_locations(prm, before_stop)
    after_stop_outbound, after_stop_rewardzone, after_stop_homebound = vr_track_location_analysis.split_locations(prm, after_stop)
    # make example power spectras
    vr_track_location_analysis.stop_start_power_spectra_locations(prm,before_stop_outbound, before_stop_rewardzone, before_stop_homebound,after_stop_outbound, after_stop_rewardzone, after_stop_homebound, channel) # FIGURE 2 B :
    # pull data from whole recording
    vr_power_calculations.calculate_and_plot_pooled_gamma_power_stop_start_locations(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel)
    # plot example continuous data
    vr_track_location_plots.make_stop_start_locations_continuous_plot(prm, channel, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound)

    return before_stop_outbound, before_stop_rewardzone, before_stop_homebound,after_stop_outbound, after_stop_rewardzone, after_stop_homebound


def process_movement_and_stationary_locations_hit_miss(prm,before_stop_outbound, before_stop_rewardzone, before_stop_homebound,after_stop_outbound, after_stop_rewardzone, after_stop_homebound, channel):
    #above based on hit or miss
    #split based on hit and miss
    bs_outbound_hit, bs_outbound_miss = vr_split_data.split_all_data_hit_miss(prm, before_stop_outbound)
    as_outbound_hit, as_outbound_miss = vr_split_data.split_all_data_hit_miss(prm, after_stop_outbound)
    bs_rz_hit, bs_rz_miss = vr_split_data.split_all_data_hit_miss(prm, before_stop_rewardzone)
    as_rz_hit, as_rz_miss = vr_split_data.split_all_data_hit_miss(prm, after_stop_rewardzone)
    bs_homebound_hit, bs_homebound_miss = vr_split_data.split_all_data_hit_miss(prm, before_stop_homebound)
    as_homebound_hit, as_homebound_miss = vr_split_data.split_all_data_hit_miss(prm, after_stop_homebound)
    # make example power spectras
    vr_track_location_analysis.stop_start_power_spectra_locations_hit_miss(prm,bs_outbound_hit, bs_outbound_miss, as_outbound_hit,as_outbound_miss, bs_rz_hit, bs_rz_miss, as_rz_hit, as_rz_miss, bs_homebound_hit, bs_homebound_miss, as_homebound_hit, as_homebound_miss, channel) # FIGURE 2 B :
    # pull data from whole recording
    vr_power_calculations.calculate_and_plot_pooled_gamma_power_stop_start_locations_hit_miss(prm, bs_outbound_hit, bs_outbound_miss, as_outbound_hit,as_outbound_miss, bs_rz_hit, bs_rz_miss, as_rz_hit, as_rz_miss, bs_homebound_hit, bs_homebound_miss, as_homebound_hit, as_homebound_miss, channel)
    # plot example continuous data
    vr_track_location_plots.make_stop_start_locations_hit_miss_continuous_plot(prm, channel, bs_outbound_hit, bs_outbound_miss, as_outbound_hit,as_outbound_miss, bs_rz_hit, bs_rz_miss, as_rz_hit, as_rz_miss, bs_homebound_hit, bs_homebound_miss, as_homebound_hit, as_homebound_miss)


def hit_miss_power_calculations(prm,data, channel):
    #power calculations
    #avg plots
    vr_power_calculations.calculate_power_hit_miss(prm,data, channel)
    vr_power_calculations.calculate_power_hit_miss_success(prm,data, channel)
    vr_power_calculations.calculate_power_hit_miss_locations(prm,data, channel)
    vr_power_calculations.calculate_power_hit_miss_success_locations(prm,data, channel)


def speed_versus_gamma_power(prm,data, channel):
    #plot avg speed against gamma power (area under PDS curve)
    vr_power_calculations.calculate_power_versus_speed(prm,data, channel)
    #speed versus power for hit and miss trials
    vr_power_calculations.calculate_power_speed_hit_miss(prm,data, channel)
    vr_power_calculations.calculate_power_speed_hit_miss_success(prm,data, channel)
    vr_power_calculations.calculate_power_speed_hit_miss_locations(prm,data, channel)

    #plot power spectra for different speed quartiles
    #upper,middle_upper, middle_lower, lower = vr_track_location_analysis.power_spectra_speed(prm,data[1000000:75000000,:], channel)
    #vr_track_location_analysis.power_spectra_speed_locations(prm,upper,middle_upper, middle_lower, lower, channel)

    #above based on hit or miss trials
    #vr_track_location_analysis.hit_miss_power_spectra_speed(prm,before_stop, after_stop, middle_upper,upper, middle_lower, lower, channel)


