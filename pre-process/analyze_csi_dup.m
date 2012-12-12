
function analyze_csi_dup(file_name1, file_name2, file_name3)
	addpath('./matlab');


	%% ---------------------------------------
	% constant
	STORE_CSI = 1;


	%% ---------------------------------------
	% variable
	output_dir = '../ChanTraces/';
	input_dir = '../rawTrace/';
	% input_dir = '~/csi_measurement/csi_measurement/raw_data/robust_MIMO/face/';
	% input_dir = '/var/local/swati/TrajectoryMeasurementDec2/';
	figure_dir = './figures/';
	% input_dir = '/u/owais/condor/power/ChanTraces/';
	% input_dir = '../raw_data/static_card2/';
	% input_dir = '../raw_data/swati_tmp/';
	% file_name = 'sender1_lap1_seg1.dat';

	
	%% ---------------------------------------
	% load traces
	raw_data1 = [input_dir file_name1];
	raw_data2 = [input_dir file_name2];
	raw_data3 = [input_dir file_name3];
	

	csi_trace1 = read_bf_file(raw_data1);
	csi_trace2 = read_bf_file(raw_data2);
	csi_trace3 = read_bf_file(raw_data3);
	csi_entry1 = csi_trace1{100}
	csi_entry2 = csi_trace2{100}
	csi_entry3 = csi_trace3{100}
	

	%% ---------------------------------------
	% parameters
	num_tx = 3;
	num_rx = 3;
	num_subcarriers = size(csi_entry1.csi, 3)
	num_observations = min([size(csi_trace1, 1), size(csi_trace2, 1), size(csi_trace3, 1)]);
	fprintf('%d * %d * %d * %d\n', num_tx, num_rx, num_subcarriers, num_observations);
	
	size(csi_trace1, 1)
	size(csi_trace2, 1)
	size(csi_trace3, 1)
	return
	
	%% ---------------------------------------
	% variable to store data
	subcarrier_csi_over_time = zeros(num_tx, num_rx, num_subcarriers, num_observations);
	

	for i = 1:num_observations
		csi_entry1 = csi_trace1{i};
		csi_entry2 = csi_trace2{i};
		csi_entry3 = csi_trace3{i};

		%% subcarriers CSI
		csi1 = get_scaled_csi(csi_entry1);
		csi2 = get_scaled_csi(csi_entry2);
		csi3 = get_scaled_csi(csi_entry3);
		subcarrier_csi_over_time(1, :, :, i) = csi1(:, :, :);
		subcarrier_csi_over_time(2, :, :, i) = csi2(:, :, :);
		subcarrier_csi_over_time(3, :, :, i) = csi3(:, :, :);
	end


	%% ---------------------------------------
	% remove initial phase
	% process_type = 'first';
	% process_type = 'average';
	process_type = 'pre_angle';
	subcarrier_csi_over_time = process_csi(subcarrier_csi_over_time, process_type);
	

	%% ---------------------------------------
	% store the CSI for Owais power project
	num_observations
	if STORE_CSI == 1
		length_to_store = num_observations; % 100;	% num_observations
		csi = zeros(length_to_store, num_tx, num_rx, num_subcarriers);
		for obs_i = 1:length_to_store
			csi(obs_i, :, :, :) = subcarrier_csi_over_time(:, :, :, obs_i);
		end

		save([output_dir file_name1 '_mix.mat'], 'csi');
	end
	





%% process_csi: function description
function [subcarrier_csi_over_time] = process_csi(subcarrier_csi_over_time, process_type)
	[num_tx, num_rx, num_subcarriers, num_observations] = size(subcarrier_csi_over_time);
	for ntx = 1:num_tx
		for nrx = 1:num_rx
			for no = 1:num_observations
				if strcmp(process_type, 'average')
					sum_phase = 0;
					for nsub = 1:num_subcarriers
						sum_phase = sum_phase + angle(subcarrier_csi_over_time(ntx, nrx, nsub, no));
					end
					avg_phase = sum_phase / nsub;
					R = abs(subcarrier_csi_over_time(ntx, nrx, :, no));
					theta = angle(subcarrier_csi_over_time(ntx, nrx, :, no));
					theta = theta - avg_phase;
					subcarrier_csi_over_time(ntx, nrx, :, no) = R .* exp(i*theta);
				elseif strcmp(process_type, 'first')
					first_phase = angle(subcarrier_csi_over_time(ntx, nrx, 1, no));
					R = abs(subcarrier_csi_over_time(ntx, nrx, :, no));
					theta = angle(subcarrier_csi_over_time(ntx, nrx, :, no));
					theta = theta - first_phase;
					subcarrier_csi_over_time(ntx, nrx, :, no) = R .* exp(i*theta);
				elseif strcmp(process_type, 'pre_angle')
					if(no ~= 1)
						x = subcarrier_csi_over_time(ntx, nrx, :, no-1);
						y = subcarrier_csi_over_time(ntx, nrx, :, no);

						phase = angle(x .* conj(y));
						y = y .* exp(phase*1j);

						subcarrier_csi_over_time(ntx, nrx, :, no) = y(1, 1, :, 1);
					end
				end
			end
		end
	end

			


	