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

    def predict(self) -> bool:
        jump = (self.state == TwoBitPredictorState.WEAK_TAKE) or (self.state == TwoBitPredictorState.STRONG_TAKE)
        return jump

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


def get_branch_history() -> List[bool]:
    import random
    return[ random.randint(0, 1) == 1 for _ in range(100) ]

def simulate(history: List[bool], predictor: TwoBitPredictor) -> float:
    hit_count = 0
    for jumped in history:
        # make prediction
        prediction = predictor.predict()
        
        branch_result = BranchResult.JUMP if jumped else BranchResult.NO_JUMP
        prediction_result = PredictionResult.CORRECT if (prediction == jumped) else PredictionResult.INCORRECT

        # check prediction
        if prediction == jumped:
            hit_count +=1

        # update predictor state
        predictor.update_state(branch_result=branch_result, prediction_result=prediction_result)

        print(f"jumped: {jumped}, prediction: {prediction}, next_state: {predictor.state}")
         
    return hit_count / len(history)

if __name__ == "__main__":
    predictor_1 = TwoBitPredictorByBranchResult()
    predictor_2 = TwoBitPredictorByPredictionResult()

    branch_history = get_branch_history()

    hit_rate_1 = simulate(branch_history, predictor_1)
    print(hit_rate_1)

    hit_rate_2 = simulate(branch_history, predictor_2)
    print(hit_rate_2)
