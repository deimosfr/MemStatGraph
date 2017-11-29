# MemStatGraph

![example1](https://raw.githubusercontent.com/deimosfr/MemStatGraph/master/images_examples/number.png)

## Information

Memcached graph stats generated with GnuPlot on linux.

This tool was quickly and dirty developed to render graph from Memcached stats with less dependency as possible and in one of the simplest way as possible.

## Dependancies

- gnuplot
- python
- pyaml

## Usage

Edit stats.yaml file and set the stats you want to graph:
```yaml
- number
- number_hot
- number_warm
- number_cold
- number_cold
- age
- evicted
- evicted_nonzero
- evicted_time
- outofmemory
- tailrepairs
- reclaimed
- expired_unfetched
- evicted_unfetched
- crawler_reclaimed
- crawler_items_checked
- lrutail_reflocked
- moves_to_cold
- moves_to_warm
- moves_within_lru
- direct_reclaims
```

Then you can pipe memcached stats output directly:
```bash
ssh server "echo 'stats items' | nc 127.0.0.1 11225" | ./mem_stat_graph.py
```
You'll find all graphs in your current directory in png format.

You can find rendering examples in images_examples folder.
