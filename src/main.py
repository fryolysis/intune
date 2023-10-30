# MIDI FACTS
# note range: 0-127 where 0 is C-1 and a step is a semitone
# pitch bend range -8191 to 8192, mapping to cents is unspecified
# channel range 0-15, pitch bend is applied to channels not notes

import utils
import weights
import analytic


# MAIN
messages = utils.preprocess()
scale = analytic.solve(weights.freq_weight(messages), weights.interval_weight)