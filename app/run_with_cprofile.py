import cProfile  # pragma: no cover
import pstats  # pragma: no cover

import uvicorn  # pragma: no cover


def main(): # pragma: no cover
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False, loop="asyncio")


if __name__ == "__main__": # pragma: no cover
    profiler = cProfile.Profile()
    profiler.runcall(main)
    stats = pstats.Stats(profiler).sort_stats(pstats.SortKey.TIME)
    stats.dump_stats("profile_stats.prof")
