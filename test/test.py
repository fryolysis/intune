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
    def test_freq_weight(self):
        for _ in range(20):
            sample = set(random.choices(range(12), k=random.randint(1,11)))
            complement = set(range(12)).difference(sample)
            mock_score = midigen.from_pitch_set(sample, 20)
            w = weights.freq_weight(mock_score)
            for i in complement:
                for j in complement:
                    self.assertAlmostEqual(w[i][j], 0)

if __name__ == '__main__':
    unittest.main()