import unittest, random, numpy
from intune.test import midigen
from intune.src import weights, solve

            

class TestWeightMethods(unittest.TestCase):
    # any weighting scheme must assign 0 weight to (x,y) where x or y never appears in the score.
    def __test_missing_pitches(self, scheme):
        sample = set(random.choices(range(12), k=random.randint(1,11)))
        complement = set(range(12)).difference(sample)
        mock_score = midigen.from_pitch_set(sample, 20)
        w = scheme(mock_score)
        for i in complement:
            for j in complement:
                self.assertAlmostEqual(w[i][j], 0)
                self.assertAlmostEqual(w[i][j], 0)
    

    def __test_simultaneity(self, scheme):
        mock_score = midigen.no_overlap(20)
        w = scheme(mock_score, window_size=1e-5)
        n = len(w)
        for i in range(n):
            for j in range(i+1,n):
                self.assertAlmostEqual(w[i][j], 0)

    def test_weighting_scheme(self):
        for _ in range(10):
            self.__test_missing_pitches(weights.mixed_weight)
            self.__test_simultaneity(weights.mixed_weight)


class TestAnalytic(unittest.TestCase):
    def test_scale_size(self):
        for _ in range(10):
            mock_pair_weight = numpy.random.random([12,12])
            mock_interval_weight = [random.random() for _ in range(12)]
            scl = solve.solve(mock_pair_weight, mock_interval_weight)
            self.assertEqual(len(scl), 11, f'Scale is:\n{scl}')
    
    def test_missing_pitches(self):
        for _ in range(10):
            mock_interval_weight = [random.random() for _ in range(12)]
            mock_pair_weight = numpy.random.random([12,12])
            missing = random.choices(range(1,12), k=random.randint(1,11))
            for m in missing:
                mock_pair_weight[m,:] = 0
                mock_pair_weight[:,m] = 0
            scl = solve.solve(mock_pair_weight, mock_interval_weight)
            try:
                self.assertEqual(len(scl), 11)
                for m in missing:
                    self.assertAlmostEqual(scl[m-1], m*100)
            except AssertionError:
                print(scl)

if __name__ == '__main__':
    unittest.main()