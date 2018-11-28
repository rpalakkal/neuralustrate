import json
with open('data2.json') as f:
    data = json.load(f)
keys = data['net'].keys()
toBePaired=[]
for item in keys:
    array=[]
    if len(data['net'][item]['connection']['input'])>0:
        x=data['net'][item]['connection']['input'][0]
    else:
        x=''

    if len(data['net'][item]['connection']['output'])>0:
        y=data['net'][item]['connection']['output'][0]
    else:
        y=''
    toBePaired.append([item, x, y])


def sort(list, layers):
    lastLayer=layers[-1][1]
    for item in list:
        if list[lastLayer][2]==item[0]:
            layers.append([item[0], list.index(item)])
            break

def order(pairIndex):
    orderedLayers=[]
    m=0
    for item in pairIndex:
        if item[1]=='':
            lastLayer=pairIndex.index(item) #this is the input layer
            orderedLayers.append([item[0], pairIndex.index(item)])
    while m<len(pairIndex):
        sort(pairIndex, orderedLayers )
        m+=1


    return orderedLayers
sortedLayers=order(toBePaired)
combinedLayers = ['ReLU', 'PReLU', 'LRN', 'TanH', 'BatchNorm', 'Dropout', 'Scale']
dataLayers = ['ImageData', 'Data', 'HDF5Data', 'Input', 'WindowData', 'MemoryData', 'DummyData']
if data['net'][sortedLayers[1][0]]['info']['type'] in dataLayers:
    sortedLayers.remove(sortedLayers[1])
for item in sortedLayers:
    print(data['net'][item[0]]['info']['type'], data['net'][item[0]]['params'])
architecture=[]
for item in sortedLayers:
    if data['net'][item[0]]['info']['type'] in combinedLayers:
        pass
    elif data['net'][item[0]]['info']['type'] in dataLayers:
        if 'dim' in data['net'][item[0]]['params']:
            x = data['net'][item[0]]['params']['dim'].split(', ')
            x = list(map(int,x))
            del x[0]
            architecture.append(x)
        elif 'batch_size' in data['net'][item[0]]['params']:
            x = int(data['net'][item[0]]['params']['batch_size'])
            architecture.append([x,64,64])
    elif data['net'][item[0]]['info']['type']=='Convolution':
        if data['net'][item[0]]['params']['layer_type']=='2D':
            numberOfSquares=int(data['net'][item[0]]['params']['num_output'])
            if 'padding_w' in data['net'][item[0]]['params']:
                squareWidth=int(data['net'][item[0]]['info']['type']['kernel_w'])+int(data['net'][item[0]]['info']['type']['padding_w'])
            else:
                squareWidth=int(data['net'][item[0]]['params']['kernel_w'])
            stride=int(data['net'][item[0]]['params']['stride_w'])
            architecture.append([numberOfSquares, squareWidth, stride])
print(architecture)
