import unittest, random
from intune.test import midigen
from intune.src import weights


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

if __name__ == '__main__':
    unittest.main()