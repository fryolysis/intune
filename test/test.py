import unittest, random, numpy
from intune.test import midigen
from intune.src import weights, solve, output


class TestWeightMethods(unittest.TestCase):

    def __test_missing_pitches(self, scheme):
        '''
        A weighting scheme must assign 0 weight to pitch class pair (x,y) where x or y never appears in the score.
        '''
        sample = set(random.choices(range(12), k=random.randint(1,11)))
        complement = set(range(12)).difference(sample)
        mock_score = midigen.from_pitch_set(sample, 20)
        w = scheme(mock_score)
        for i in complement:
            for j in complement:
                self.assertAlmostEqual(w[i][j], 0)
                self.assertAlmostEqual(w[i][j], 0)
    

    def __test_simultaneity(self, scheme):
        '''
        A weighting scheme with infinitesimal window size must return zero weight matrix for a monophonic score.
        '''
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
    
    def test_scale(self):
        for _ in range(10):
            mock_interval_weight = [random.random() for _ in range(12)]
            mock_pair_weight = numpy.random.random([12,12])
            missing = random.choices(range(12), k=random.randint(0,11))
            for m in missing:
                mock_pair_weight[m,:] = 0
                mock_pair_weight[:,m] = 0
            sol = solve.solve(mock_pair_weight, mock_interval_weight)
            scl = output.align(sol)
            # check scale size
            self.assertEqual(len(scl), 11)
            # check ordering
            self.assertEqual(scl, sorted(scl))
            # check missing pitches
            for m in missing:
                # first pitch is implicitly 0 and not included in scl
                if m==0:
                    continue
                self.assertAlmostEqual(scl[m-1], m*100, 
                    msg=f'scl[{m-1}] = {scl[m-1]} != {m*100}'
                )

if __name__ == '__main__':
    unittest.main()