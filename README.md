
# Earthquake Python Rest API

A Rest API developed in python using fast api to collect data from USGS services




## Deployment

To deploy this project

clone the github repository
```bash
  git clone https://github.com/lmmfs/earth.git
```
start the services

```bash
  docker compose up
```


## API Reference

#### Get most recent earthquake records

```http
  GET /earthquakes
```


#### Get earthquake record

```http
  GET /earthquakes/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of record to fetch |


