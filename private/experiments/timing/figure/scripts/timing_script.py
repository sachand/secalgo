import sys, os, subprocess, time, json

full_path = '/home/christopher/secalgo/experiments/timing/figure/'
result_path = '/home/christopher/secalgo/experiments/timing/figure/results/'
output_path = '/home/christopher/secalgo/experiments/timing/figure/output/'
m_buf_opt = '--message-buffer-size'
m_buf_size = '65536'
da_ext = '.da'
results_ext = '_results.txt'
error_ext = '_error.log'

protocols = ['ns-sk_fixed_rk',
             'ns-sk_fixed_fk',
             'pc_ns-sk_fixed_rk',
             'pc_ns-sk_fixed_fk']
#             'ns-sk_fixed_rn',
#             'ns-sk_fixed_fn']

testsizes = ['1250', '2500', '5000', '10000', '15000', '20000', '25000']
#testsizes = ['100', '200', '300', '400', '500']
#testsizes = ['1250', '2500']

def time_exp(loops, iter_num):
    print('Protocol Timing Experiment - Varied Data Size', flush = True)
    for p in protocols:
        for i in range(iter_num):
            print('Iteration ' + str(i + 1) + ':', flush = True)
            for ts in testsizes:
                print('Test Data Size -- ' + ts + ':', flush = True)
                cmd = ['python3', '-m', 'da', m_buf_opt, m_buf_size,
                       full_path + p + da_ext, str(loops), ts]
                print('Running:', cmd, flush = True)
                f_txt = open(result_path + p + '_' + ts + '_' +
                             str(i + 1) + results_ext, 'w')
                f_err = open(result_path + p + '_' + ts + '_' +
                             str(i + 1) + error_ext, 'w')
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
    print('Completed Protocol Timing Experiment - Varied Data Size', flush = True)
#end time_exp01()

def parse_exp(iter_num, output_file):
    for p in protocols:
        if output_file == None:
            of = open(output_path + p + '_output.txt', 'w')
        else:
            of = open(output_file, 'w')
        results = dict()
        results[p] = p
        #print('Results for:', p, file = of, flush = True)
        print('Results for:', p, flush = True)
        for ts in testsizes:
            avg_protocol_time = 0
            total_protocol_time = 0
            iter_result_list = []
            for i in range(iter_num):
                protocol_time = 0
                with open(result_path + p + '_' + ts +'_' +
                          str(i + 1) + results_ext, 'r') as f:
                    for read_line in f:                    
                        data_line = json.loads(read_line)
                        #print(data_line, file = of, flush = True)
                        #print(data_line, flush = True)
                        role_time = ((data_line[3] - data_line[2]) / data_line[4])
                        #print('role time:', data_line[0], ':', data_line[1], '-', role_time,
                        #      file = of, flush = True)
                        #print('role time:', data_line[0], ':', data_line[1], '-', role_time,
                        #      flush = True)
                        protocol_time += role_time
                iter_result = [(i + 1), p, ts, (protocol_time * 1000)]
                iter_result_list.append(iter_result)
                #print(json.dumps(iter_result), file = of, flush = True)
                print(json.dumps(iter_result), flush = True)
                results[ts] = iter_result_list
            for ir in iter_result_list:
                total_protocol_time += ir[3]
            avg_protocol_time = total_protocol_time / iter_num
            results[ts + '_avg'] = avg_protocol_time
            print('avg for ' + p + ', ' + ts + ':', total_protocol_time, '/', iter_num, '=',
              avg_protocol_time, flush = True)
        print(results)
        title_line = 'Results for -- Protocol running time for NS-SK,'
        title_line += ' with increasing key size, :'
        file_line = 'File: ' + results[p] + da_ext
        sizes_line = ''
        iter_lines = [''] * iter_num
        h_line = '-' * 70
        avg_line = ''
        cols_desc = 'Columns: Size of new session key in bytes.'
        rows_desc = 'Rows: Total protocol running time (sum of each particpant' 
        rows_desc += ' process running time) in\nmiliseconds (of CPU time),'
        rows_desc += ' averaged over 1000 executions of each protocol.'
        avg_desc = 'Average running time of protocol over 10 runs of the experiment.'
        for ts1 in testsizes:
            if ts1 == '5000':
                sizes_line += '\t' + ts1
            else:
                sizes_line += '\t\t' + ts1
            for i1 in range(iter_num):
                iter_lines[i1] += '\t' + str(round(results[ts1][i1][3], 6))
            avg_line += '\t' + str(round(results[ts1 + '_avg'], 6))
        print(title_line, file = of)
        print(file_line + '\n', file = of)
        print('Size' + sizes_line, file = of)
        cntr = 1
        for line in iter_lines:
            print('R' + str(cntr) + line, file = of)
            cntr += 1
        print(h_line, file = of)
        print('AVG' + avg_line, file = of)
        print('\n' + cols_desc, file = of)
        print('\n' + rows_desc, file = of)
        print('\n' + avg_desc, file = of)
        of.close()
#end parse_exp()

if __name__ == '__main__':
    loops = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    iter_num = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    time_exp(loops, iter_num)
    parse_exp(iter_num, output_file)