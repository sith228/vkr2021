# TCP packet structure

## Contents

* [Packet structure](##Packet-structure)
* [Events](##Events)
* [Data structure](##Data-structure)
  * [BUS_DETECTION, BUS_ROUTE_NUMBER_RECOGNITION, BUS_DOOR_DETECTION](###BUS_DETECTION,-BUS_ROUTE_NUMBER_RECOGNITION,-BUS_DOOR_DETECTION)
    * [Image formats](#Image-formats)
  * [BUS_DETECTION_RESULT, BUS_ROUTE_NUMBER_RECOGNITION_RESULT, BUS_DOOR_DETECTION_RESULT](###BUS_DETECTION_RESULT,-BUS_ROUTE_NUMBER_RECOGNITION_RESULT,-BUS_DOOR_DETECTION_RESULT)

## Packet structure

| Segment     | Offset in bytes |
|:-----------:|:---------------:|
| Event       | 0               |
| Token       | 1               |
| Data length | 17              |
| Data        | 21              |

## Events

| Code | Mode                                | Purpose                         |
|:----:|:-----------------------------------:|:-------------------------------:|
| 0    | INIT_SESSION                        | Initialize session              |
| 63   | CLOSE_SESSION                       | Coles session                   |
| 64   | BUS_DETECTION                       | Run bus detection               |
| 65   | BUS_ROUTE_NUMBER_RECOGNITION        | Run route number recognition    |
| 66   | BUS_DOOR_DETECTION                  | Run bus door detection          |
| 128  | SESSION_OK                          | Initialize session OK           |
| 192  | BUS_DETECTION_RESULT                | Bus detection result            |
| 193  | BUS_ROUTE_NUMBER_RECOGNITION_RESULT | Route number recognition result |
| 194  | BUS_DOOR_DETECTION_RESULT           | Bus door detection result       |

## Data structure

### BUS_DETECTION, BUS_ROUTE_NUMBER_RECOGNITION, BUS_DOOR_DETECTION

| Segment      | Offset in bytes |
|:------------:|:---------------:|
| Height       | 0               |
| Width        | 2               |
| Image format | 4               |
| Image        | 5               |

#### Image formats

|Code | Format  |
|:---:|:-------:|
| 0   | RAW_BGR |
| 1   | JPG_RGB |

### BUS_DETECTION_RESULT, BUS_ROUTE_NUMBER_RECOGNITION_RESULT
| Segment      | Offset in bytes |
|:------------:|:---------------:|
| Control      | 0               |
| Bus boxes    | 1               |

### Bus box
| Segment      | Offset in bytes |
|:------------:|:---------------:|
| x            | 0               |
| y            | 4               |
| Height       | 8               |
| Width        | 12              |
| Text length  | 16              |
| Text         | 20              |