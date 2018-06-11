import csv
from dallinger.experiments import Griduniverse

ROWS = 49
COLS = 49
ORIG_CSV_LIMIT = csv.field_size_limit(ROWS*COLS*1024)

BASE_ID = "{}01daa{}-f7ed-43fa-ad6b-9928aa51f8e1"
PARTICIPANTS = 9
NUM_AS_EXPERIMENTS = 3
NUM_RANDOM_EXPERIMENTS = 3

EXP_CONFIG = {
    "recruiter": "bots",
    "max_participants": PARTICIPANTS,
}

exp = Griduniverse()
data = {}

print('Collecting {} experiments with {} AdvantageSeekingBot players'.format(
    NUM_AS_EXPERIMENTS, PARTICIPANTS
))

for count in range(NUM_AS_EXPERIMENTS):
    exp_id = BASE_ID.format('ab', count)
    config = EXP_CONFIG.copy()
    config['bot_policy'] = 'AdvantageSeekingBot'
    data[exp_id] = {
        'title': '{} Experiment #{} ({})'.format(config['bot_policy'],
                                                 count + 1, exp_id),
        'data': exp.collect(exp_id, exp_config=config)
    }

print('Collecting {} experiments with {} RandomBot players'.format(
    NUM_RANDOM_EXPERIMENTS, PARTICIPANTS
))

for count in range(NUM_RANDOM_EXPERIMENTS):
    exp_id = BASE_ID.format('ad', count)
    config = EXP_CONFIG.copy()
    config['bot_policy'] = 'RandomBot'
    data[exp_id] = {
        'title': '{} Experiment #{} ({})'.format(config['bot_policy'],
                                                 count + 1, exp_id),
        'data': exp.collect(exp_id, exp_config=config)
    }

print(
    'Successfully collected data from '
    '{} bot experiments. Rendering replay widgets:'.format(
        len(data))
)
