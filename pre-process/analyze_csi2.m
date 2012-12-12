
function analyze_csi(file_name)
	addpath('../matlab');


	%% ---------------------------------------
	% constant
	STORE_CSI = 1;


	%% ---------------------------------------
	% variable
	output_dir = './OUTPUT/';
	input_dir = '../raw_data/mobile_trace/';
	% input_dir = '/u/yichao/tmp2/';
	% input_dir = '../raw_data/static_card2/';
	% input_dir = '../raw_data/swati_tmp/';

	
	%% ---------------------------------------
	% load traces
	% raw_data = '../raw_data/robust_MIMO/face/office.0.01m.data';
	% raw_data = '../raw_data/mac/20120715.data';
	% raw_data = '../raw_data/static_card2/card2.6m.data';
	% raw_data = '../raw_data/mobile_trace/face.speed3.data';
	% raw_data = '../raw_data/robust_MIMO/side/';
	% raw_data = '../raw_data/mobile_trace/face.speed1.data';
	% raw_data = '../raw_data/swati_tmp/l1.dat';
	% file_name = 'face.speed1.data';
	% file_name = 'face.speed2.data';
	% file_name = 'face.speed3.data';
	% file_name = 'side.speed1.data';
	% file_name = 'side.speed2.data';
	% file_name = 'side.speed3.data';
	% file_name = 'card2.6m.data';
	% file_name = 'l1.dat';
	raw_data = [input_dir file_name];


	load(raw_data, 'CSI');
	

	% csi_trace = read_bf_file(raw_data);
	% csi_entry = csi_trace{100}
	

	%% ---------------------------------------
	% parameters
	[num_observations, num_tx, num_rx, num_subcarriers] = size(CSI);
	% num_tx = csi_entry.Ntx;
	% num_rx = csi_entry.Nrx;
	% num_subcarriers = size(csi_entry.csi, 3);
	% num_observations = size(csi_trace, 1);


	%% ---------------------------------------
	% verify if the parameters remain within the whole trace
	% XXX: do it here!



	%% ---------------------------------------
	% variable to store data
	% antenna_csi_over_time = zeros(num_rx, num_observations);
	% subcarrier_csi_over_time = zeros(num_tx, num_rx, num_subcarriers, num_observations);
	% pkt_intervals = zeros(num_observations-1, 1);
	 
	for obs_i = 1:num_observations
		subcarrier_csi_over_time(:, :, :, obs_i) = CSI(obs_i, :, :, :);
	end
	

	% pre_time = 0;
	% for i = 1:num_observations
	% 	csi_entry = csi_trace{i};

	% 	%% antenna RSSI
	% 	assert(num_rx == 3);
	% 	antenna_csi_over_time(1, i) = csi_entry.rssi_a;
	% 	antenna_csi_over_time(2, i) = csi_entry.rssi_b;
	% 	antenna_csi_over_time(3, i) = csi_entry.rssi_c;

	% 	%% subcarriers CSI
	% 	csi = get_scaled_csi(csi_entry);
	% 	% for ntx = 1:num_tx
	% 	% 	for nrx = 1:num_rx
	% 	% 		subcarrier_csi_over_time(ntx, nrx, :, i) = csi(ntx, nrx, :);
	% 	% 	end
	% 	% end
	% 	subcarrier_csi_over_time(:, :, :, i) = csi(:, :, :);

	% 	%% packet arrival interval
	% 	if(i == 1)
	% 		pre_time = csi_entry.timestamp_low;
	% 	else
	% 		pkt_intervals(i-1, 1) = csi_entry.timestamp_low - pre_time;
	% 		% assert(pkt_intervals(i-1, 1) > 0);
	% 		pre_time = csi_entry.timestamp_low;
	% 	end
	% end


	%% ---------------------------------------
	% remove initial phase
	% process_type = 'first';
	% process_type = 'average';
	process_type = 'pre_angle';
	subcarrier_csi_over_time = process_csi(subcarrier_csi_over_time, process_type);
	

	%% ---------------------------------------
	% store the CSI for Owais power project
	if STORE_CSI == 1
		length_to_store = num_observations; % 100;	% num_observations
		csi = zeros(length_to_store, num_tx, num_rx, num_subcarriers);
		for obs_i = 1:length_to_store
			csi(obs_i, :, :, :) = subcarrier_csi_over_time(:, :, :, obs_i);
		end

		save([output_dir file_name '.mat'], 'csi');

		% f10 = figure;
		% plot(db(abs(csi(:, 1, 1, 1))))
		% print(f10, '-dpsc', 'tmp1.ps')
		% f11 = figure;
		% plot(angle(csi(:, 1, 1, 1)))
		% print(f11, '-dpsc', 'tmp2.ps')
		% tmp = squeeze(subcarrier_csi_over_time(1, 1, 1, 1:length_to_store))
		% f12 = figure;
		% plot(db(abs(tmp)))
		% print(f12, '-dpsc', 'tmp3.ps')
		% f13 = figure;
		% plot(angle(tmp))
		% print(f13, '-dpsc', 'tmp4.ps')
	end
	


	%% ---------------------------------------
	% plot
	% plot_start = 1000;
	% plot_end = 1003;
	% plot_subcarrier_start = 1;
	% plot_subcarrier_end = 1;
	% %% fig 1. antenna rssi over time
	% f1 = figure;
	% plot(antenna_csi_over_time(:, plot_start:plot_end)');
	% legend('RX Antenna A', 'RX Antenna B', 'RX Antenna C', 'Location', 'SouthEast' );
	% xlabel('packet');
	% ylabel('RSSI [dB]');
	% print(f1, '-dpsc', 'antenna_rssi.ps')

	% %% fig 2. subcarrier csi over time
	% %% fig 3. subcarrier phase over time
	% %% fig 7. subcarrier phase over time 2
	% for ntx = 1:num_tx
	% 	for nrx = 1:num_rx
	% 		f2 = figure;
	% 		plot(db(abs(squeeze(subcarrier_csi_over_time(ntx, nrx, plot_subcarrier_start:plot_subcarrier_end, :)).')));
	% 		xlabel('packet');
	% 		ylabel('SNR [dB]');
	% 		% axis([0 80 0 50]);
	% 		print(f2, '-dpsc', ['subcarrier_rssi_tx' int2str(ntx) '_rx' int2str(nrx) '.ps']);

	% 		f3 = figure;
	% 		% plot(angle(squeeze(subcarrier_csi_over_time(ntx, nrx, plot_subcarrier_start:plot_subcarrier_end, plot_start:plot_end)).'));
	% 		plot(angle(squeeze(subcarrier_csi_over_time(ntx, nrx, plot_subcarrier_start:plot_subcarrier_end, :)).'));
	% 		xlabel('packet');
	% 		ylabel('phase (radian)');
	% 		% axis([0 80 -4 4]);
	% 		print(f3, '-dpsc', ['subcarrier_phase_tx' int2str(ntx) '_rx' int2str(nrx) '.ps']);

	% 		f7 = figure;
	% 		tmp = reshape(subcarrier_csi_over_time(ntx, nrx, 1:30, plot_start:plot_end), 30*(plot_end-plot_start+1), 1);
	% 		% tmp = reshape(subcarrier_csi_over_time(ntx, nrx, 1:30, [2001:1000:5001]), 30*(4), 1);
	% 		plot(angle(tmp),'-*');
	% 		xlabel(['30 subcarriers of ' int2str(plot_end-plot_start+1) 'packets']);
	% 		ylabel('phase (radian)');
	% 		print(f7, '-dpsc', ['subcarrier_phase_tx' int2str(ntx) '_rx' int2str(nrx) '_2.ps']);
	% 	end
	% end

	% %% fig4. packet arrival interval
	% f4 = figure;
	% [f,x] = ecdf(pkt_intervals(plot_start:plot_end));
	% stairs(x, f, 'LineWidth', 2)
	% xlabel('interval (us)');
	% ylabel('CDF');
	% print(f4, '-dpsc', 'pkt_interval_cdf.ps')

	% %% fig5. 2D plot of symbols: amplitude & phase
	% f5 = figure;
	% num_pkt = 3;
	% pkt_start = 1;
	% x = zeros(num_subcarriers * num_pkt, 1);
	% y = zeros(num_subcarriers * num_pkt, 1);
	% group = zeros(num_subcarriers * num_pkt, 1);
	% for pkt = pkt_start:pkt_start+num_pkt-1
	% 	H = zeros(30, 1);
	% 	H(:, 1) = subcarrier_csi_over_time(1, 1, 1:30, pkt);
	% 	x((pkt-pkt_start)*num_subcarriers+1:(pkt-pkt_start+1)*num_subcarriers, 1) = real(H);
	% 	y((pkt-pkt_start)*num_subcarriers+1:(pkt-pkt_start+1)*num_subcarriers, 1) = imag(H);
	% 	group((pkt-pkt_start)*num_subcarriers+1:(pkt-pkt_start+1)*num_subcarriers, 1) = pkt;
	% end
	% gscatter(x, y, group)
	% print(f5, '-dpsc', ['pkt_sybols.ps']);

	
	%% fig6. 2D plot of symbols: amplitude & phase
	% shift_subcarrier_csi_over_time = process_csi(subcarrier_csi_over_time);
	% f6 = figure;
	% num_pkt = 3;
	% pkt_start = 1000;
	% x = zeros(num_subcarriers * num_pkt, 1);
	% y = zeros(num_subcarriers * num_pkt, 1);
	% group = zeros(num_subcarriers * num_pkt, 1);
	% for pkt = pkt_start:pkt_start+num_pkt-1
	% 	H = zeros(30, 1);
	% 	H(:, 1) = shift_subcarrier_csi_over_time(1, 1, 1:30, pkt);
	% 	x((pkt-pkt_start)*num_subcarriers+1:(pkt-pkt_start+1)*num_subcarriers, 1) = real(H);
	% 	y((pkt-pkt_start)*num_subcarriers+1:(pkt-pkt_start+1)*num_subcarriers, 1) = imag(H);
	% 	group((pkt-pkt_start)*num_subcarriers+1:(pkt-pkt_start+1)*num_subcarriers, 1) = pkt;
	% end
	% gscatter(x, y, group)
	% print(f6, '-dpsc', ['pkt_sybols_shift_phase.ps']);


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

			


	