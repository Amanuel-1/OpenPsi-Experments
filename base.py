from pydantic import BaseModel, Field
import math


class Stv(BaseModel):
    """A second-order probability construct (Simple Truth Value)"""


    PRIOR_ALPHA: float = 0.5
    PRIOR_BETA: float = 0.5
    LOOK_AHEAD: float = 1.0
    MAX_COUNT: float = 1e9


    probability: float = Field(..., ge=0.0, le=1.0, description="Mode of beta distribution")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence")


    count: float = 0.0
    positive_count: float = 0.0



    def confidence_to_count(self):
        """Update count, positive_count from confidence"""
        if math.isclose(self.confidence, 1.0, abs_tol=1e-9):
            self.count = self.MAX_COUNT
        else:
            self.count = (self.confidence * self.LOOK_AHEAD) / (1 - self.confidence)
        self.positive_count = self.probability * self.count
        return self

    def count_to_confidence(self):
        """Update confidence from count"""
        self.confidence = self.count / (self.count + self.LOOK_AHEAD)
        self.positive_count = self.probability * self.count
        return self

    def increment_negative_count(self):
        """Increase negative evidence (only count increases)"""
        self.confidence_to_count()
        self.count += 1
        self.confidence = self.count / (self.count + self.LOOK_AHEAD)
        self.probability = self.positive_count / self.count if self.count > 0 else 0
        return self

    def increment_positive_count(self):
        """Increase positive evidence (both positive and total counts increase)"""
        self.confidence_to_count()
        self.count += 1
        self.positive_count += 1
        self.confidence = self.count / (self.count + self.LOOK_AHEAD)
        self.probability = self.positive_count / self.count
        return self

    def cog_mean(self) -> float:
        """Expected probability (mean of Beta distribution)"""
        a = self.post_alpha()
        b = self.post_beta()
        return a / (a + b)

    def beta_distribution(self) -> tuple[float, float]:
        """Return posterior (alpha, beta) for the Beta distribution"""
        return self.post_alpha(), self.post_beta()

    # --- Internal helpers ---
    def post_alpha(self) -> float:
        return self.PRIOR_ALPHA + self.positive_count

    def post_beta(self) -> float:
        return self.PRIOR_BETA + (self.count - self.positive_count)


class CogScm(BaseModel):
    """A cognitive schema carrying a truth value"""
    weight: float
    context: str
    action: str
    goal: str
    goalValue: str
    tv: Stv











