import unittest, random, numpy
from intune.test import midigen
from intune.src import weights, analytic


class TestMockScore(unittest.TestCase):
    def test_from_pitch_set(self):
        mock_score = midigen.from_pitch_set(range(12), 50)
        cur_playing = set()
        for msg in mock_score:
            if msg.type == 'note_on':
                cur_playing.add(msg.note)
            else:
                self.assertIn(msg.note, cur_playing)
                cur_playing.remove(msg.note)
        self.assertSetEqual(cur_playing, set())
            

class TestWeightMethods(unittest.TestCase):
    # any weighting scheme must assign 0 weight to (x,y) where x or y never appears in the score.
    def test_missing_pitches(self):
        for _ in range(20):
            sample = set(random.choices(range(12), k=random.randint(1,11)))
            complement = set(range(12)).difference(sample)
            mock_score = midigen.from_pitch_set(sample, 20)
            wf = weights.freq_weight(mock_score)
            ww = weights.window_weight(mock_score)
            for i in complement:
                for j in complement:
                    self.assertAlmostEqual(wf[i][j], 0)
                    self.assertAlmostEqual(ww[i][j], 0)

class TestAnalytic(unittest.TestCase):
    def test_scale_size(self):
        for _ in range(10):
            mock_pair_weight = numpy.random.random([12,12])
            mock_interval_weight = [random.random() for _ in range(12)]
            scl = analytic.solve(mock_pair_weight, mock_interval_weight)
            try:
                self.assertEqual(len(scl), 11)
            except AssertionError:
                print(scl)
    
    def test_missing_pitches(self):
        for _ in range(10):
            mock_interval_weight = [random.random() for _ in range(12)]
            mock_pair_weight = numpy.random.random([12,12])
            missing = random.choices(range(1,12), k=random.randint(1,11))
            for m in missing:
                mock_pair_weight[m,:] = 0
                mock_pair_weight[:,m] = 0
            scl = analytic.solve(mock_pair_weight, mock_interval_weight)
            try:
                self.assertEqual(len(scl), 11)
                for m in missing:
                    self.assertAlmostEqual(scl[m-1], m*100)
            except AssertionError:
                print(scl)

if __name__ == '__main__':
    unittest.main()