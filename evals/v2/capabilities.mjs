// Capability -> skill names that satisfy it, per arm.
// A capability passes when any listed skill is loaded via the skill tool,
// or when its SKILL.md is read from disk (the v2 registry route).
export const capabilities = {
  baseline: {
    'router': ['admin', 'research-admin', 'code-admin', 'workbench-admin', 'skill-router'],
    'paper.single': ['paper-read', 'paper-triage', 'paper-method'],
    'paper.method': ['paper-method'],
    'paper.cross': ['paper-synthesize'],
    'evidence.citation': ['citation-guard'],
    'evidence.claim': ['hallucination-guard', 'verification-before-completion', 'self-evaluator'],
    'experiment.reproduce': ['paper-to-notebook', 'run-on-modal'],
    'code.debug': ['debug-investigator', 'code-senior'],
    'research.assess': ['research-admin', 'ieee-q1-devil-advocate', 'paper-method'],
    'web.design': ['design-web', 'web-admin', 'design-ui-direction'],
    'study.handbook': ['study-forge'],
  },
  v2: {
    'router': ['admin'],
    'paper.single': ['paper-read'],
    'paper.method': ['paper-read'],
    'paper.cross': ['paper-synthesize'],
    'evidence.citation': ['evidence-check'],
    'evidence.claim': ['evidence-check'],
    'experiment.reproduce': ['experiment'],
    'code.debug': ['code-senior'],
    'research.assess': ['research-assess'],
    'web.design': ['design-web'],
    'study.handbook': ['study-forge'],
  },
};
