"""
Encapsulate generate data to make it parallel
"""
from os import makedirs
from os.path import join
import argparse
from multiprocessing import Pool
from subprocess import call

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rollouts', type=int, help="Total number of rollouts.")
    parser.add_argument('--threads', type=int, help="Number of threads")
    parser.add_argument('--rootdir', type=str, help="Directory to store rollout "
                        "directories of each thread")
    parser.add_argument('--policy', type=str, choices=['brown', 'white'],
                        help="Directory to store rollout directories of each thread",
                        default='brown')
    args = parser.parse_args()

    rpt = args.rollouts // args.threads  # 修改1: 去掉 +1，精确分配

    with Pool(args.threads) as p:
        # 修改2: 使用 partial 或 lambda 将 args 传递给子函数
        from functools import partial
        p.map(partial(_threaded_generation, args=args, rpt=rpt), range(args.threads))

    
def _threaded_generation(i, args, rpt):  # 修改3: 增加 args 和 rpt 参数
    tdir = join(args.rootdir, 'thread_{}'.format(i))
    makedirs(tdir, exist_ok=True)
    
    # 修改4: 使用列表形式传递参数，避免字符串拼接和引号问题
    cmd = [
        # 'xvfb-run', # comment out since I'm using MacOS
        # '-s', '-screen 0 1400x900x24',  # 去掉多余的嵌套引号
        # '--server-num={}'.format(i + 1),
        'python', '-m', 'data.carracing',
        '--dir', tdir,
        '--rollouts', str(rpt),
        '--policy', args.policy
    ]
    
    print(' '.join(cmd))
    call(cmd)  # 修改5: 去掉 shell=True，直接传列表更安全

if __name__ == '__main__':
    main()