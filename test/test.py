import unittest, random, numpy
from intune.test import midigen
from intune.src import weights, solve, output, main


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


class TestSolutions(unittest.TestCase):
    def test_compatibility(self):
        for _ in range(10):
            pset = set(random.choices(range(12), k=6))
            score = midigen.from_pitch_set(pset, 800)
            winsize = random.random()*5
            main.fixedmode(score, winsize=winsize)
            fixedsol = score.solution
            print(fixedsol)
            main.varmode(score, forgetbef=1e5, winsize=winsize)
            varsol = score.solution
            print(varsol)
            idtocls = [note.cls for note in score.varid_to_note]
            for k,v in varsol.items():
                if idtocls[k] > 0:
                    self.assertAlmostEqual(fixedsol[idtocls[k]-1], v)
            print('passed')


if __name__ == '__main__':
    unittest.main()