import { RepositoryState, GitEngine } from '@/lib/git/engine';
import { Mission, Objective } from '@/store/gameStore';

/**
 * Checks if a specific objective is met based on the current Git state.
 * Returns true if the objective is completed.
 */
export function checkObjective(objectiveId: string, state: RepositoryState): boolean {
  const engine = new GitEngine(state);
  
  switch (objectiveId) {
    case 'init':
      // Has HEAD and a refs/heads/main branch initialized
      return !!state.refs['refs/heads/main'] || !!state.head;

    case 'add':
      // Has at least one file in the staging area (index)
      return Object.keys(state.index).length > 0;

    case 'commit':
      // Has at least one commit
      return Object.keys(state.objects).some(k => state.objects[k].type === 'commit');

    case 'branch':
      // Has multiple branches or specifically 'feature-login'
      return Object.keys(state.refs).length > 1 || !!state.refs['refs/heads/feature-login'];

    case 'checkout':
      // Is currently on a branch other than main
      return state.head !== 'refs/heads/main' && state.head.startsWith('refs/heads/');

    default:
      return false;
  }
}

/**
 * Validates the entire mission to see if all objectives are completed
 */
export function isMissionComplete(mission: Mission, state: RepositoryState): boolean {
  return mission.objectives.every(obj => checkObjective(obj.id, state));
}
