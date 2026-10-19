# Reasoning check (shared by research-assess and evidence-check)

Most confirmed errors in past research sessions were not missing sources but wrong
inferences from correct sources (NCKH T07 post-mortem: 11 of 14 errors). Run these six
questions on every derived, causal or universal claim before accepting it.

1. **Scope of the result.** What exactly does the theorem, table or source guarantee, and
   what does the claim use it for? (A lattice theorem guarantees a grid point inside a box;
   it says nothing about detection recall.)
2. **Bound type.** Is the number an upper bound, lower bound, expectation or a single
   observation? Is the claim using it as that type?
3. **Counter-example.** Can you build one concrete case, ideally with a few lines of
   arithmetic or code, where the premise holds and the conclusion fails?
4. **Control.** For a causal claim ("module X causes the gain"), was only X changed? List
   every other change made in the same run (epochs, augmentation, seed, data).
5. **Same problem class.** Does the cited source study the same task, data regime and
   metric as the claim?
6. **Depth vs strength.** Was the source read deeply enough for the strength of the
   wording ("no prior work", "only", "solves")? See depth labels in `evidence.md`.

Output per claim: `claim → giữ / thu hẹp / bác` + the question that decided it + the
evidence (file:line, table, run). Report "đã kiểm suy luận" only for claims that went
through all six questions.
