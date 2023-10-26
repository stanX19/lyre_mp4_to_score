import unittest
import numpy as np
from srcs.deduce_key_pos import deduce_all_key_pos

class MyTestCase(unittest.TestCase):
    def test_3_rows(self):
        sample = [[604, 414, 72, 71, 0.7], [715, 414, 72, 71, 0.7], [603, 499, 72, 71, 0.7], [713, 499, 72, 71, 0.7],
                  [266, 500, 72, 71, 0.7], [378, 500, 72, 71, 0.7], [491, 500, 72, 71, 0.7], [825, 500, 72, 71, 0.7],
                  [937, 500, 72, 71, 0.7], [265, 585, 72, 71, 0.7], [377, 585, 72, 71, 0.7], [490, 585, 72, 71, 0.7],
                  [717, 586, 72, 71, 0.7], [823, 586, 72, 71, 0.7], [935, 586, 72, 71, 0.7], [606, 587, 72, 71, 0.7]]
        positions = deduce_all_key_pos(sample, 1280, 720)
        self.assertEqual(21, len(positions))

    def test_uncertainty(self):
        sample = [[609, 637, 93, 91, 0.9], [750, 637, 93, 91, 0.9], [1315, 637, 93, 91, 0.9], [1456, 637, 93, 91, 0.9], [891, 638, 93, 91, 0.9], [1032, 638, 93, 91, 0.9], [1175, 640, 93, 91, 0.9],
                  [610, 750, 93, 91, 0.9], [751, 750, 93, 91, 0.9], [1456, 750, 93, 91, 0.9], [890, 751, 93, 91, 0.9], [1031, 751, 93, 91, 0.9], [1174, 751, 93, 91, 0.9], [1314, 751, 93, 91, 0.9],
                  [608, 864, 93, 91, 0.9], [750, 864, 93, 91, 0.9], [892, 864, 93, 91, 0.9], [1033, 864, 93, 91, 0.9], [1174, 864, 93, 91, 0.9], [1316, 864, 93, 91, 0.9], [1456, 864, 93, 91, 0.9]]

        for i in range(0, 100):  # np.arange(0.0, 7.0, 0.001):
            positions = deduce_all_key_pos(sample, 1280, 720, i)
            if positions is not sample:
                max_uncertain = 10
                self.assertLessEqual(i, max_uncertain,
                                     f"deduce_all_key_pos requires uncertainty {i}>{max_uncertain} on sample")
                break

if __name__ == '__main__':
    unittest.main()
