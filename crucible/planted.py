"""Planted-leak fixtures (T15): every gating probe must FIRE on a generator
variant with its leak deliberately planted, or its silence on the real
generator certifies nothing.  A silent-pass probe is a failed audit."""
from . import constants as C
from .gen import generate_corpus
from .engine import Engine
from . import policies as PL
from . import audits as A

EPS = 160   # planted runs use a 160-episode prefix (spans nothing frozen)


def _rows(leak=None, dyn=None, episodes=EPS):
    corpus = generate_corpus(C.EVAL_SEEDS[0], leak=leak, episodes=episodes)
    eng = Engine(corpus, PL.NullEmpty(seed=90017), **({"dyn": dyn} if dyn
                                                      else {}))
    eng.run()
    return eng, A.scored_rows(eng)


def run_all():
    out = {}
    # PL1: appearance encodes kind -> A4 must fail
    _, rows = _rows(leak="appearance")
    r = A.a4_appearance(rows)
    out["PL1_appearance"] = {"probe_fired": not r["pass"], "evidence": r}
    # PL2: display order sorted by kind -> A8 must fail
    _, rows = _rows(leak="token")
    r = A.a8_token_position(rows)
    out["PL2_token"] = {"probe_fired": not r["pass"], "evidence": r}
    # PL3: ambient targeting becomes a hard single-kind label.  The real
    # confound is itself strongly kind-correlated by declaration, so the
    # kind-excess MAGNITUDE cannot separate confound from label (measured
    # differential ~0.045 on matched windows — a silent fixture).  The
    # STRUCTURE can: real draft-heat and rain-soak target different
    # attribute sets (overlap only on rare B), a planted label targets one
    # kind for both.  Fire iff the cross-type targeting-overlap rate under
    # the planted variant exceeds the real generator's by > 0.15.
    real_corpus = generate_corpus(C.EVAL_SEEDS[0], episodes=EPS)
    plant_corpus = generate_corpus(C.EVAL_SEEDS[0], leak="ambient",
                                   episodes=EPS)
    real_rate = A.ambient_crosstype_overlap(real_corpus)
    plant_rate = A.ambient_crosstype_overlap(plant_corpus)
    fired = (plant_rate - real_rate) > 0.15
    out["PL3_ambient"] = {"probe_fired": fired,
                          "evidence": {"real_overlap_rate": real_rate,
                                       "planted_overlap_rate": plant_rate}}
    # PL4: outcome-frequency beacon at E_R -> A6 must fail.
    from . import dyn_a

    class Beacon:
        f1 = staticmethod(dyn_a.f1)
        f2 = staticmethod(dyn_a.f2)

    class BeaconShift:
        """post-E_R soak 'null' becomes 'dissolve' (side-channel beacon)."""
        current_ep = [0]

        @classmethod
        def f1(cls, alpha, cond, action):
            out, nc = dyn_a.f1(alpha, cond, action)
            if (action == "soak" and out == "null"
                    and cls.current_ep[0] >= C.E_R):
                return "dissolve", nc
            return out, nc

        f2 = staticmethod(dyn_a.f2)

    corpus = generate_corpus(C.EVAL_SEEDS[0],
                             episodes=min(C.EPISODES, C.E_R + 100))

    class TrackingEngine(Engine):
        def _episode(self, epi):
            BeaconShift.current_ep[0] = epi["episode"]
            super()._episode(epi)

    eng = TrackingEngine(corpus, PL.NullEmpty(seed=90017), dyn=BeaconShift)
    eng.run()
    r = A.a6_shift_invisibility(eng)
    out["PL4_outcome_beacon"] = {"probe_fired": not r["pass"], "evidence": r}
    # PL5: cracked arrivals from episode 1 -> A10 must fail
    corpus = generate_corpus(C.EVAL_SEEDS[0], leak="cracked_early",
                             episodes=EPS)
    r = A.a10_scans({C.EVAL_SEEDS[0]: corpus})
    out["PL5_cracked_early"] = {"probe_fired": not r["pass"], "evidence": r}
    out["pass"] = all(v["probe_fired"] for k, v in out.items()
                      if k.startswith("PL"))
    return out
