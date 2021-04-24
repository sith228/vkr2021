# TCP packet structure

## Contents

* [Header structure](##Header-structure)
* [Events](##Events)
* [Data structure](##Data-structure)
  * [BUS_DETECTION, BUS_ROUTE_NUMBER_RECOGNITION, BUS_DOOR_DETECTION](###BUS_DETECTION,-BUS_ROUTE_NUMBER_RECOGNITION,-BUS_DOOR_DETECTION)
    * [Image formats](#Image-formats)
  * [BUS_DETECTION_RESULT, BUS_ROUTE_NUMBER_RECOGNITION_RESULT, BUS_DOOR_DETECTION_RESULT](###BUS_DETECTION_RESULT,-BUS_ROUTE_NUMBER_RECOGNITION_RESULT,-BUS_DOOR_DETECTION_RESULT)

## Header structure

| Segment     | Offset in bytes |
| :----------:| :-------------: |
| Event       | 0               |
| Token       | 1               |
| Data length | 17              |
| Data        | 21              |

## Events

| Code | Mode                                | Purpose                         |
| :--: | :---------------------------------: | :-----------------------------: |
| 0    | INIT_SESSION                        | Initialize session              |
| 1    | BUS_DETECTION                       | Run bus detection               |
| 2    | BUS_ROUTE_NUMBER_RECOGNITION        | Run route number recognition    |
| 3    | BUS_DOOR_DETECTION                  | Run bus door detection          |
| 4    | BUS_DETECTION_RESULT                | Bus detection result            |
| 5    | BUS_ROUTE_NUMBER_RECOGNITION_RESULT | Route number recognition result |
| 6    | BUS_DOOR_DETECTION_RESULT           | Bus door detection result       |
| 255  | CLOSE_SESSION                       | Coles session                   |

## Data structure

### BUS_DETECTION, BUS_ROUTE_NUMBER_RECOGNITION, BUS_DOOR_DETECTION

| Segment      | Offset in bytes |
| :-----------:| :-------------: |
| Height       | 0               |
| Width        | 2               |
| image format | 4               |
| Image        | 5               |

#### Image formats

|Code | Format |
| :-: | :----: |

### BUS_DETECTION_RESULT, BUS_ROUTE_NUMBER_RECOGNITION_RESULT, BUS_DOOR_DETECTION_RESULT
