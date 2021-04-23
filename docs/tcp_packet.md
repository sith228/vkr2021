#TCP packet structure

## Overview

## Header structure

| Header     | Offset |
| :---------:| :----: |
| Mode       | 0      |
| Token      | 1      |
| Data length| 17     |
| Data       | 21     |

## Modes

| Mode                         | Purpose                      |
| :--------------------------: | :--------------------------: |
| INIT_SESSION                 | Initialize session           |
| BUS_DETECTION                | Run bus detection            |
| BUS_ROUTE_NUMBER_RECOGNITION | Run route number recognition |
| BUS_DOOR_DETECTION           | Run bus door detection       |

## Data structure
### BUS_DETECTION, BUS_ROUTE_NUMBER_RECOGNITION, BUS_DOOR_DETECTION

| Header      | Offset |
| :----------:| :----: |
| Height      | 0      |
| Width       | 2      |
| Color depth | 4      |
| Image       | 5      |
