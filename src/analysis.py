# pylint: disable=missing-docstring,invalid-name

from display import draw_graph, draw_histogram
from formats import factory

import matplotlib.pyplot as plt
import numpy as np


def analysis():
    data = [
        # 'dat/board0x70_Channel0to15_20210311_InjectCharge.dat',
        # 'dat/board0x70_Channel16to31_20210311_InjectCharge.dat',
        # 'dat/board0x70_Channel32to47_20210311_InjectCharge.dat',
        # 'dat/board0x70_Channel48to63_20210311_InjectCharge.dat',
    ]

    squash = factory['auto']()

    # pedes = []
    # gains = []

    # for group in zip(*[iter(data)] * 4):
    #     for f in group:
    #         _, _, _, pars, _ = squash.parser(f, output='signal')

    #         pedes.append(pars[:,0])
    #         gains.append(pars[:,1])

    # np_pedes = np.concatenate(pedes)
    # np_gains = np.concatenate(gains)

    # # print(np_pedes)
    # # print(np_gains)

    # # distribution of pedestals
    # draw_histogram(np_pedes, 50, labels=('pedestal', 'counts'),
    #     xrange=(1300, 1800, 100), yrange=(0, 50, 5))

    # # distribution of gains
    # draw_histogram(np_gains, 25, labels=('gains', 'counts'),
    #     xrange=(90, 115, 5), yrange=(0, 100, 10))

    ###########################################################################

    for group in zip(*[iter(data)] * 1):
        board_id = 'BOARDID'

        _m = np.zeros((40, 0, 28))
        _s = np.zeros((40, 0, 28))
        _y = np.zeros((0, 40))
        _p = np.zeros((0, 2))
        _e = np.zeros((0, 2))

        for f in group:
            mean, sigma, y, pars, errs = squash.parser(f, output='signal')

            _m = np.concatenate((_m, mean), axis=1)
            _s = np.concatenate((_s, sigma), axis=1)
            _y = np.vstack((_y, y))
            _p = np.vstack((_p, pars))
            _e = np.vstack((_e, errs))

        yp = np.array(_p[:,0])
        yg = np.array(_p[:,1])

        # ---------------------------------------------------------------------
        # draw pulse maximum vs steps
        pulse_max_vs_step_disp_opts = {
            'yrange': (0, 18000, 4000),
            'interval': 4,
            'labels': ('pulse #', 'pulse maximum'),
            'fmt_str': [
                'board {}',
                'channel {}',
                '[{:.0f}, {:.0f}]',
            ],
            'fmt_data': [
                [(board_id,)] * _y.shape[0],
                list(zip(range(_y.shape[0]))),
                pars.tolist(),
            ],
            'output': 'pulse_max_vs_step_board_{}'.format(board_id),
        }

        draw_graph(_y, None, **pulse_max_vs_step_disp_opts)

        # ---------------------------------------------------------------------
        # draw pulse shapes for all steps for a single channel
        pulse_vs_sample_disp_opts = {
            'yrange': (0, 18000, 4000),
            'interval': 4,
            'labels': ('sample #', 'ADC value'),
            'fmt_str': [
                'board {}',
                'channel {}',
                'pulse {}',
            ],
            'fmt_data': [
                [(board_id,)] * _m.shape[0],
                None,
                list(zip(range(_m.shape[0]))),
            ],
            'output': None,
        }

        for c in range(_m.shape[1]):
            pulse_vs_sample_disp_opts['fmt_data'][1] = [(c,)] * _m.shape[0]
            pulse_vs_sample_disp_opts['output'] = \
                'pulse_vs_sample_board_{}_channel_{}.png'.format(board_id, c)
            draw_graph(_m[:,c,:], sigma[:,c,:], **pulse_vs_sample_disp_opts)

        # ---------------------------------------------------------------------
        # draw pedestal vs channel
        pedestal_vs_channel_disp_opts = {
            'yrange': (0, 2000, 200),
            'interval': 4,
            'labels': ('channel', 'pedestal'),
            'fmt_str': ['board {}'],
            'fmt_data': [(board_id,)],
            'output': 'pedestal_vs_channel_board_{}'.format(board_id),
        }

        draw_graph(yp, None, **pedestal_vs_channel_disp_opts)

        # ---------------------------------------------------------------------
        # draw gain vs channel
        gain_vs_channel_disp_opts = {
            'yrange': (0, 400, 50),
            'interval': 4,
            'labels': ('channel', 'gain'),
            'fmt_str': ['board {}'],
            'fmt_data': [(board_id,)],
            'output': 'gain_vs_channel_board_{}'.format(board_id),
        }

        draw_graph(yg, None, **gain_vs_channel_disp_opts)


if __name__ == '__main__':
    analysis()
