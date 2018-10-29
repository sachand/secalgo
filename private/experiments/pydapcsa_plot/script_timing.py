import sys, os, subprocess, time, json, argparse
#from sa import secalgoB.useTimers
#from sa import secalgoB.proto_loops
#from sa import sec_algo_pycrypto.usePickleTimer
#from sa import sec_algo_pycrypto.pickle_loops
import sa.secalgoB as SA
import sa.sec_algo_pycrypto as SA_PyCrypto
sa_path = '/home/christopher/secalgo/'
signal_path = '/home/christopher/secalgo-org/examples/signal/'
full_path = sa_path + 'ProtocolImplementations/New/'
raw_path = sa_path + 'experiments/pydapcsa_plot/rawData/'
results_path = sa_path + 'experiments/pydapcsa_plot/results/'
m_buf_opt = '--message-buffer-size'
m_buf_size = '8192'
da_ext = '.da'
results_ext = '_results.txt'
error_ext = '_error.log'

#protocols = ['ns-sk_fixedT', 'pc_ns-sk_fixedT', 'pc_ns-sk_fixedL', 'pc_ns-sk_fixedP']
protocols = ['dsT',
             'ds-pkT',
             'ns-skT',
             'ns-sk_fixedT',
             'ns-pkT',
             'orT',
             'wlT',
             'yaT',
             'dhke-1T',
             'sdhT',
             'tls1_2T',
             'kerberos5T',
             'pc_ns-sk_fixedL',
             'pc_ns-sk_fixedT',
             'x3dhT']

sec_algo_functions = ('keygen',
                      'encrypt',
                      'decrypt',
                      'sign',
                      'verify',
                      'nonce',
                      'BitGen',
                      'key_derivation',
                      'local_pow',
                      'tls_prf_sha256',
                      'encode',
                      'decode',
                      'kdf',
                      'dh')

p_main_skip = {'dsT'             : 2,
               'ds-pkT'          : 3,
               'ns-skT'          : 2,
               'ns-sk_fixedT'    : 2,
               'ns-pkT'          : 3,
               'orT'             : 2,
               'wlT'             : 2,
               'yaT'             : 2,
               'dhke-1T'         : 7,
               'sdhT'            : 3,
               'tls1_2T'         : 4,
               'kerberos5T'      : 4,
               'pc_ns-sk_fixedL' : 0,
               'x3dhT'           : 0}


def measure_proto_time(p, iter_num, iter_label):
    print('Protocol Timing Experiment for:', p, flush = True)
    if p in protocols:
        if p == 'dhke-1T' or p == 'ds-pkT' or p == 'sdhT' or p == 'tls1_2':
            cmd = ['python3', '-m', 'da', m_buf_opt, m_buf_size,
                   full_path + p + da_ext]
        elif p == 'x3dhT':
            cmd = ['python3', '-m', 'da', signal_path + p + da_ext]
        else:
            cmd = ['python3', '-m', 'da', full_path + p + da_ext]
        print('Running:', cmd, flush = True)
        if iter_num:
            the_range = range(iter_num)
        else:
            the_range = range((iter_label - 1), iter_label)        
        for i in the_range:
            print('Iteration ' + str(i + 1) + ':', flush = True)
            f_txt = open(raw_path + 'protocol/' + p + '_' + str(i + 1) + results_ext, 'w')
            f_err = open(raw_path + 'protocol/' + p + '_' + str(i + 1) + error_ext, 'w')
            child = subprocess.Popen(cmd, bufsize= -1, stdout = f_txt,
                                     stderr = f_err, universal_newlines = True)
            child.wait()
            #stdout, stderr = child.communicate()
            #print(stdout, flush = True)
            f_txt.close()
            f_err.close()
            
            time.sleep(1)
            print('Completed Iteration', str(i + 1), flush = True)
        print('Finished', p, flush = True)
        print('Completed Protocol Timing Experiment for:', p, flush = True)
    else:
        print('No such protocol', p, 'available.', flush = True)
#end measure_proto_time()

def parse_proto_time(p, iter_num, iter_label, output_file):
    if output_file == None:
        of = open(results_path + 'protocol/' + p + '_output.txt', 'w')
    else:
        of = open(output_file, 'w')
    if p in protocols:
        print('Results for:', p, file = of, flush = True)
        total_protocol_time = 0
        role_times = []
        iter_result_list = []
        if iter_num:
            iter_count = iter_num
        else:
            iter_count = iter_label
        for i in range(iter_count):
            protocol_time = 0
            with open(raw_path + 'protocol/' + p + '_' + str(i + 1) + results_ext, 'r') as f:
                for read_line in f:                    
                    data_line = json.loads(read_line)
                    #print(data_line, file = of, flush = True)
                    print(data_line, flush = True)
                    role_time = (data_line[3] - data_line[2])
                    #print('role time:', data_line[0], ':', data_line[1], '-', role_time,
                    #      file = of, flush = True)
                    role_times.append(((i+1), data_line[1], role_time))
                    protocol_time += role_time
            protocol_time = protocol_time
            iter_result = [(i + 1), p, protocol_time]
            iter_result_list.append(iter_result)
            #print(json.dumps(iter_result), file = of, flush = True)
        for ir in iter_result_list:
            total_protocol_time += ir[2]
        total_protocol_time = total_protocol_time
        avg_protocol_time = total_protocol_time / iter_count
        for rt in role_times:
            print(str(rt[0]) + '\t' + rt[1] + '\t' + str(rt[2]), file = of, flush = True)
        for irt in iter_result_list:
            print(str(irt[0]) + '\t' + irt[1] + '\t' + str(irt[2]), file = of, flush = True)
        print(json.dumps(['avg', p, total_protocol_time, iter_count, 
                          avg_protocol_time]), file = of, flush = True)
        print('avg for ' + p + ':', total_protocol_time, '/', iter_count, '=',
              avg_protocol_time, flush = True)
        of.close()
#end parse_proto_time()

def measure_lib_time(p, iter_num, iter_label):
    print('Library Timing Experiment for:', p, flush = True)
    if p in protocols:
        if p == 'dhke-1T' or p == 'ds-pkT' or p == 'sdhT' or p == 'tls1_2T':
            cmd = ['python3', '-m', 'da', m_buf_opt, m_buf_size, full_path + p + da_ext]
        elif p == 'x3dhT':
            cmd = ['python3', '-m', 'da', signal_path + p + da_ext]
        else:
            cmd = ['python3', '-m', 'da', full_path + p + da_ext]
        print('Running:', cmd, flush = True)
        if iter_num:
            the_range = range(iter_num)
        else:
            the_range = range((iter_label - 1), iter_label)
        for i in the_range:
            print('Iteration ' + str(i + 1) + ':', flush = True)
            f_txt = open(raw_path + 'library/' + p + '_' + str(i + 1) + results_ext, 'w')
            f_err = open(raw_path + 'library/' + p + '_' + str(i + 1) + error_ext, 'w')
            child = subprocess.Popen(cmd, bufsize= -1, stdout = f_txt,
                                     stderr = f_err, universal_newlines = True)
            child.wait()
            #stdout, stderr = child.communicate()
            #print(stdout, flush = True)
            f_txt.close()
            f_err.close()

            time.sleep(1)
            print('Completed Iteration', str(i + 1), flush = True)
        print('Finished', p, flush = True)
        print('Completed Library Timing Experiment for:', p, flush = True)
    else:
        print('No such protocol', p, 'available.', flush = True)
#end measure_lib_time()

def parse_lib_time(p, iter_num, iter_label, output_file):
    if output_file == None:
        of = open(results_path + 'library/' + p + '_output.txt', 'w')
    else:
        of = open(output_file, 'w')
    if p in protocols:
        print('Results for:', p, file = of, flush = True)
        total_library_time = 0
        function_times = []
        iter_result_list = []
        function_skip = p_main_skip[p]
        if iter_num:
            iter_count = iter_num
        else:
            iter_count = iter_label
        for i in range(iter_count):
            library_time = 0
            skip_counter = 0
            with open(raw_path + 'library/' + p + '_' + str(i + 1) + results_ext, 'r') as f:
                for read_line in f:
                    data_line = json.loads(read_line)
                    #print(data_line, file = of, flush = True)
                    if data_line[0] in sec_algo_functions:
                        #print('library', file = of, flush = True)
                        if ((data_line[0] == 'keygen' or data_line[0] == 'sign') and
                            skip_counter < function_skip):
                            #print('skip', file = of, flush = True)
                            print('SKIP:', data_line, flush = True)
                            skip_counter += 1
                        else:
                            function_time = (((data_line[2] - data_line[1]) / data_line[3])
                                             * 1000)
                            #print('function time:', data_line[0], '-', function_time,
                            #      file = of, flush = True)
                            function_times.append(((i+1), data_line[0], function_time))
                            print(str(i+1) + ': ' + data_line[0] + ':', data_line[2],
                                  '-', data_line[1], '/', data_line[3], '=',
                                  function_time, flush = True)
                            library_time += function_time
            iter_result = [(i + 1), p, library_time]
            iter_result_list.append(iter_result)
            #print(json.dumps(iter_result), file = of, flush = True)
            print(iter_result, flush = True)
        for ir in iter_result_list:
            total_library_time += ir[2]
        avg_library_time = total_library_time / iter_count
        for ft in function_times:
            print(str(ft[0]) + '\t' + ft[1] + '\t' + str(ft[2]), file = of, flush = True)
        for irt in iter_result_list:
            print(str(irt[0]) + '\t' + irt[1] + '\t' + str(irt[2]), file = of, flush = True)
        print(json.dumps(['avg', p, total_library_time, iter_count, avg_library_time]),
              file = of, flush = True)
        print('avg for ' + p + ':', total_library_time, '/', iter_count, '=',
              avg_library_time, flush = True)
        of.close()
#end parse_lib_time()

def measure_pickle_time(p, iter_num, iter_label):
    print('Pickle Timing Experiment for:', p, flush = True)
    if p in protocols:
        if p == 'dhke-1T' or p == 'ds-pkT' or p == 'sdhT' or p == 'tls1_2T':
            cmd = ['python3', '-m', 'da', m_buf_opt, m_buf_size,
                   full_path + p + da_ext]
        else:
            cmd = ['python3', '-m', 'da', full_path + p + da_ext]
        print('Running:', cmd, flush = True)
        if iter_num:
            the_range = range(iter_num)
        else:
            the_range = range((iter_label - 1), iter_label)        
        for i in the_range:
            print('Iteration ' + str(i + 1) + ':', flush = True)
            f_txt = open(raw_path + 'pickle/' + p + '_' + str(i + 1) + results_ext, 'w')
            f_err = open(raw_path + 'pickle/' + p + '_' + str(i + 1) + error_ext, 'w')
            child = subprocess.Popen(cmd, bufsize= -1, stdout = f_txt,
                                     stderr = f_err, universal_newlines = True)
            child.wait()
            #stdout, stderr = child.communicate()
            #print(stdout, flush = True)
            f_txt.close()
            f_err.close()
            
            time.sleep(1)
            print('Completed Iteration', str(i + 1), flush = True)
        print('Finished', p, flush = True)
        print('Completed Pickle Timing Experiment for:', p, flush = True)
    else:
        print('No such protocol', p, 'available.', flush = True)
#end measure_pickle_time()

def parse_pickle_time(p, iter_num, iter_label, output_file):
    if output_file == None:
        of = open(results_path + 'pickle/' + p + '_output.txt', 'w')
    else:
        of = open(output_file, 'w')
    if p in protocols:
        print('Results for:', p, file = of, flush = True)
        total_pickle_time = 0
        iter_result_list = []
        if iter_num:
            iter_count = iter_num
        else:
            iter_count = iter_label
        for i in range(iter_count):
            pickle_time = 0
            with open(raw_path + 'pickle/' + p + '_' + str(i + 1) + results_ext, 'r') as f:
                for read_line in f:                    
                    data_line = json.loads(read_line)
                    print(data_line, file = of, flush = True)
                    print(data_line, flush = True)
                    # miliseconds
                    fp_time = (((data_line[3] - data_line[2]) / data_line[4]) * 1000)
                    print(data_line[1], ':', data_line[0], '-', fp_time,
                          file = of, flush = True)
                    pickle_time += fp_time
            iter_result = [(i + 1), p, pickle_time]
            iter_result_list.append(iter_result)
            print(json.dumps(iter_result), file = of, flush = True)
        for ir in iter_result_list:
            total_pickle_time += ir[2]
        avg_pickle_time = total_pickle_time / iter_count
        print(json.dumps(['avg', p, total_pickle_time, iter_count, 
                          avg_pickle_time]), file = of, flush = True)
        print('avg for ' + p + ':', total_pickle_time, '/', iter_count, '=',
              avg_pickle_time, flush = True)
        of.close()
#end parse_proto_time()

def init_arg_parser():
    parser = argparse.ArgumentParser(description = 'Run timing' + 
                                     ' experiments:')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-i', '--iterations', type = int,
                       help = 'number of times protocol timing' + 
                       ' experiment will run')
    group.add_argument('-I', '--iteration-label', type = int,
                       help = 'run a single iteration with the given' + 
                       ' integer label')
    parser.add_argument('-l', '--loops', default = 1,
                        help = 'number of times each protocol will be run' +
                        ' during a single iteration of the experiment')
    parser.add_argument('-o', '--output-file',
                        help = 'name of output file')
    parser.add_argument('-t', '--test-type',
                        help = 'name of value to be measured')
    parser.add_argument('proto',
                        help = 'name of the file (sans extension) containing' + 
                        ' the protocol one wishes to run')
    return parser
#end init_arg_parser()

if __name__ == '__main__':
    parser = init_arg_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.test_type == 'protocol':
        if args.proto == 'all':
            for p in protocols:
                measure_proto_time(p, args.iterations, args.iteration_label)
                parse_proto_time(p, args.iterations, args.iteration_label, 
                                 args.output_file)
        else:
            measure_proto_time(args.proto, args.iterations, args.iteration_label)
            parse_proto_time(args.proto, args.iterations, args.iteration_label, 
                             args.output_file)
    elif args.test_type == 'library':
        if args.proto == 'all':
            for p in protocols:
                measure_lib_time(p, args.iterations, args.iteration_label)
                parse_lib_time(p, args.iterations, args.iteration_label, 
                                 args.output_file)
        else:
            measure_lib_time(args.proto, args.iterations, args.iteration_label)
            parse_lib_time(args.proto, args.iterations, args.iteration_label, 
                             args.output_file)
    elif args.test_type == 'pickle':
        if args.proto == 'all':
            for p in protocols:
                measure_pickle_time(p, args.iterations, args.iteration_label)
                parse_pickle_time(p, args.iterations, args.iteration_label, 
                                  args.output_file)
        else:
            measure_pickle_time(args.proto, args.iterations, args.iteration_label)
            parse_pickle_time(args.proto, args.iterations, args.iteration_label, 
                              args.output_file)
    else:
        print('Test type', args.test_type, 'not recognized.')
