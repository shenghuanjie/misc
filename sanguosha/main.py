# This is a sample Python script.
import argparse

# 张昌蒲算牌
# sample usage python main.py 13 6 7 1


def get_truth(length, states):
    if length == 1:
        return [[i] for i in range(states)]
    else:
        return [[i] + result for i in range(states) for result in get_truth(length - 1, states)]


def sanguosha(arr, desired=None, number_of_output=8):
    assigned = get_truth(len(arr), 3)
    sum_groups = [
        [sum([arr[idx] for idx, group in enumerate(group_id) if group == target]) for target in range(2)]
        for group_id in assigned
    ]
    has_equal = [idx for idx, groupsum in enumerate(sum_groups) if groupsum[0] == groupsum[1] and groupsum[0] != 0]
    final_sum = [sum_groups[idx][0] for idx in has_equal]
    del sum_groups
    final_groups = [[[arr[arr_idx] for arr_idx, j in enumerate(assigned[idx]) if j == i] for i in range(3)]
                    for idx in has_equal]
    del has_equal
    del assigned
    final_count = [len(group[0]) + len(group[1]) for group in final_groups]

    final_groups_string = ['|'.join(sorted([','.join(list(map(str, sorted(numbers)))) for numbers in group]))
                           for group in final_groups]

    unique_idx = [idx for idx, group in enumerate(final_groups_string)
                  if group not in final_groups_string[:idx]]

    final_groups = [final_groups[idx] for idx in unique_idx]
    final_count = [final_count[idx] for idx in unique_idx]
    final_sum = [final_sum[idx] for idx in unique_idx]

    sorted_idx = sorted(range(len(final_count)), key=final_count.__getitem__)[::-1]

    final_groups = [final_groups[idx] for idx in sorted_idx]
    final_count = [final_count[idx] for idx in sorted_idx]
    final_sum = [final_sum[idx] for idx in sorted_idx]

    for i, (group, count, sums) in enumerate(zip(final_groups, final_count, final_sum)):
        if desired is None:
            wanted = [False]
        else:
            wanted = [d in group[0] or d in group[1] for d in desired]
        if i >= number_of_output:
            break
        print(f'{"**" if all(wanted) else "* " if any(wanted) else "  "}{count}: '
              f'{"+".join(list(map(str, group[0])))} = {"+".join(list(map(str, group[1])))} = {sums}')


def get_args():
    parser = argparse.ArgumentParser(description='Sanguosha zhang pu cheng.')
    parser.add_argument('integers', type=int, nargs='+',
                        help='all cards')
    parser.add_argument('-d', '--desired', type=int, nargs='+',
                        help='priority cards.')
    parser.add_argument('-n', '--number_of_output', type=int, default=10,
                        help='The number of output to print.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    sanguosha(args.integers, desired=args.desired, number_of_output=args.number_of_output)
