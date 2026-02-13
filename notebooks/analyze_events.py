import pandas as pd

# Load raw events
df_events = pd.read_pickle('wyscout_events.pkl')

print('=' * 80)
print('POSITIONS COLUMN STRUCTURE ANALYSIS')
print('=' * 80)

# Sample different events to see position structure
sample_indices = [0, 1, 2, 10, 20, 50]

for idx in sample_indices:
    print(f'\nEvent {idx}:')
    print(f'  Event Type: {df_events.iloc[idx]["eventName"]}')
    print(f'  Sub-event: {df_events.iloc[idx]["subEventName"]}')
    print(f'  Positions: {df_events.iloc[idx]["positions"]}')

print(f'\n' + '=' * 80)
print('CHECKING FOR NULL/MISSING POSITIONS')
print('=' * 80)
print(f'Total events: {len(df_events)}')
print(f'Events with null positions: {df_events["positions"].isnull().sum()}')
print(f'Events with empty list positions: {(df_events["positions"].apply(lambda x: len(x) == 0 if isinstance(x, list) else True)).sum()}')

# Sample events with different position counts
print(f'\nDistribution of position counts per event:')
position_counts = df_events['positions'].apply(lambda x: len(x) if isinstance(x, list) else 0)
print(position_counts.value_counts().head(10))

# Show some complete examples
print(f'\n' + '=' * 80)
print('COMPLETE EXAMPLES WITH FULL DETAILS')
print('=' * 80)
for idx in range(0, 3):
    event = df_events.iloc[idx]
    positions = event['positions']
    print(f'\nEvent {idx}:')
    print(f'  Type: {event["eventName"]} / {event["subEventName"]}')
    print(f'  Team: {event["teamId"]}, Player: {event["playerId"]}')
    print(f'  Positions list length: {len(positions)}')
    if len(positions) >= 1:
        print(f'  Start position (dict): {positions[0]}')
        print(f'    - Keys in position dict: {positions[0].keys()}')
        print(f'    - X value: {positions[0].get("x")}')
        print(f'    - Y value: {positions[0].get("y")}')
    if len(positions) >= 2:
        print(f'  End position (dict): {positions[1]}')
        print(f'    - X value: {positions[1].get("x")}')
        print(f'    - Y value: {positions[1].get("y")}')

print(f'\n' + '=' * 80)
print('COORDINATE RANGES')
print('=' * 80)
# Extract all start x, y coordinates
start_xs = []
start_ys = []
end_xs = []
end_ys = []

for positions in df_events['positions']:
    if isinstance(positions, list) and len(positions) > 0:
        if 'x' in positions[0]:
            start_xs.append(positions[0]['x'])
            start_ys.append(positions[0]['y'])
        if len(positions) > 1 and 'x' in positions[1]:
            end_xs.append(positions[1]['x'])
            end_ys.append(positions[1]['y'])

print(f'Start X coordinates - Min: {min(start_xs)}, Max: {max(start_xs)}, Mean: {sum(start_xs)/len(start_xs):.2f}')
print(f'Start Y coordinates - Min: {min(start_ys)}, Max: {max(start_ys)}, Mean: {sum(start_ys)/len(start_ys):.2f}')
print(f'End X coordinates - Min: {min(end_xs)}, Max: {max(end_xs)}, Mean: {sum(end_xs)/len(end_xs):.2f}')
print(f'End Y coordinates - Min: {min(end_ys)}, Max: {max(end_ys)}, Mean: {sum(end_ys)/len(end_ys):.2f}')
