"""
Purpose:
Simulate 2-bit Predictor and measure it's hit rate.
"""

from enum import Enum
from typing import List

class BranchResult(Enum):
    JUMP = True
    NO_JUMP = False

class PredictionResult(Enum):
    CORRECT = True
    INCORRECT = False

class TwoBitPredictorState(Enum):
    STRONG_NOT_TAKE = 0
    WEAK_NOT_TAKE = 1
    WEAK_TAKE = 2
    STRONG_TAKE = 3

class TwoBitPredictor():
    def __init__(self) -> None:
        self.state: TwoBitPredictorState = TwoBitPredictorState.WEAK_NOT_TAKE

    def __repr__(self) -> str:
        return f'[state: {self.state}]'

    def set_state(self, new_state: TwoBitPredictorState) -> None:
        self.state = new_state

    def predict(self) -> BranchResult:
        jump = (self.state == TwoBitPredictorState.WEAK_TAKE) or (self.state == TwoBitPredictorState.STRONG_TAKE)
        return BranchResult.JUMP if jump else BranchResult.NO_JUMP

    def update_state(self, branch_result: BranchResult, prediction_result: PredictionResult) -> None:
        pass

class TwoBitPredictorByBranchResult(TwoBitPredictor):
    def __init__(self) -> None:
        super().__init__()
        self.state_transitions = {
            TwoBitPredictorState.STRONG_NOT_TAKE : {
                BranchResult.NO_JUMP: TwoBitPredictorState.STRONG_NOT_TAKE,
                BranchResult.JUMP: TwoBitPredictorState.WEAK_NOT_TAKE
            },
            TwoBitPredictorState.WEAK_NOT_TAKE : {
                BranchResult.NO_JUMP: TwoBitPredictorState.STRONG_NOT_TAKE,
                BranchResult.JUMP: TwoBitPredictorState.WEAK_TAKE
            },
            TwoBitPredictorState.WEAK_TAKE : {
                BranchResult.NO_JUMP: TwoBitPredictorState.WEAK_NOT_TAKE,
                BranchResult.JUMP: TwoBitPredictorState.STRONG_TAKE
            },
            TwoBitPredictorState.STRONG_TAKE : {
                BranchResult.NO_JUMP: TwoBitPredictorState.WEAK_TAKE,
                BranchResult.JUMP: TwoBitPredictorState.STRONG_TAKE
            },
        } 

    def update_state(self, branch_result: BranchResult, prediction_result: PredictionResult) -> None:
        next_state = self.state_transitions[self.state][branch_result]
        
        super().set_state(next_state)

class TwoBitPredictorByPredictionResult(TwoBitPredictor):
    def __init__(self) -> None:
        super().__init__()
        self.state_transitions = {
            TwoBitPredictorState.STRONG_NOT_TAKE: {
                PredictionResult.INCORRECT: TwoBitPredictorState.WEAK_NOT_TAKE,
                PredictionResult.CORRECT: TwoBitPredictorState.STRONG_NOT_TAKE
            },
            TwoBitPredictorState.WEAK_NOT_TAKE: {
                PredictionResult.INCORRECT: TwoBitPredictorState.WEAK_TAKE,
                PredictionResult.CORRECT: TwoBitPredictorState.STRONG_NOT_TAKE
            },
            TwoBitPredictorState.WEAK_TAKE: {
                PredictionResult.INCORRECT: TwoBitPredictorState.WEAK_NOT_TAKE,
                PredictionResult.CORRECT: TwoBitPredictorState.STRONG_TAKE
            },
            TwoBitPredictorState.STRONG_TAKE: {
                PredictionResult.INCORRECT: TwoBitPredictorState.WEAK_TAKE,
                PredictionResult.CORRECT: TwoBitPredictorState.STRONG_TAKE
            }
        }
        
    def update_state(self, branch_result: BranchResult, prediction_result: PredictionResult) -> None:
        next_state = self.state_transitions[self.state][prediction_result]
        
        super().set_state(next_state)


def get_branch_history(history_size: int = 10) -> List[BranchResult]:
    import random
    return[ BranchResult.JUMP if random.randint(0, 1) == 1 else BranchResult.NO_JUMP for _ in range(history_size) ]

def simulate(history: List[BranchResult], predictor: TwoBitPredictor, verbose: bool = False) -> float:
    hit_count = 0

    for branch_result in history:
        # make prediction
        prediction = predictor.predict()


        # check prediction
        is_prediction_correct = (prediction == branch_result)
        prediction_result = PredictionResult.CORRECT if is_prediction_correct else PredictionResult.INCORRECT
        if is_prediction_correct:
            hit_count += 1

        predictor.update_state(branch_result, prediction_result)

        if verbose:
            print(f"jumped: {branch_result}, prediction: {prediction}, next_state: {predictor.state}")
         
    return hit_count / len(history)

if __name__ == "__main__":
    predictor_with_branch_result = TwoBitPredictorByBranchResult()
    predictor_with_prediction_result = TwoBitPredictorByPredictionResult()

    branch_history = get_branch_history(history_size=1000)

    print('Predictor with Branch Result')
    hit_rate_1 = simulate(branch_history, predictor_with_branch_result)
    print(f'Hit Rate: {hit_rate_1}')

    print('Predictor with Prediction Result')
    hit_rate_2 = simulate(branch_history, predictor_with_prediction_result)
    print(f'Hit Rate: {hit_rate_2}')
