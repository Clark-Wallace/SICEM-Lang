from typing import Dict, Any, List, Optional
import json
from dataclasses import dataclass
from datetime import datetime
import numpy as np

@dataclass
class CILMetric:
    comprehension: float  # Understanding of context
    adaptation: float     # Ability to adapt content
    learning: float      # Learning from interactions
    communication: float # Communication effectiveness
    creativity: float    # Creative problem solving

@dataclass
class CILAssessment:
    intelligence_id: str
    timestamp: datetime
    metrics: CILMetric
    overall_score: float
    confidence: float
    interaction_count: int

class CILTracker:
    def __init__(self):
        self.assessments: Dict[str, List[CILAssessment]] = {}
        self.interaction_history: Dict[str, List[Dict[str, Any]]] = {}
        
    def track_interaction(self, intelligence_id: str, interaction: Dict[str, Any]):
        """Track an interaction and update CIL assessment"""
        if intelligence_id not in self.interaction_history:
            self.interaction_history[intelligence_id] = []
            
        # Add timestamp and store interaction
        interaction['timestamp'] = datetime.now().isoformat()
        self.interaction_history[intelligence_id].append(interaction)
        
        # Update CIL assessment
        self._update_assessment(intelligence_id)
        
    def _update_assessment(self, intelligence_id: str):
        """Update the CIL assessment based on interaction history"""
        interactions = self.interaction_history[intelligence_id]
        
        # Calculate metrics from interactions
        metrics = self._calculate_metrics(interactions)
        
        # Calculate overall score (weighted average)
        weights = {
            'comprehension': 0.3,
            'adaptation': 0.25,
            'learning': 0.2,
            'communication': 0.15,
            'creativity': 0.1
        }
        
        overall_score = sum(
            getattr(metrics, metric) * weight
            for metric, weight in weights.items()
        )
        
        # Calculate confidence based on interaction count
        confidence = min(1.0, len(interactions) / 100)  # More interactions = higher confidence
        
        # Create new assessment
        assessment = CILAssessment(
            intelligence_id=intelligence_id,
            timestamp=datetime.now(),
            metrics=metrics,
            overall_score=overall_score,
            confidence=confidence,
            interaction_count=len(interactions)
        )
        
        # Store assessment
        if intelligence_id not in self.assessments:
            self.assessments[intelligence_id] = []
        self.assessments[intelligence_id].append(assessment)
        
    def _calculate_metrics(self, interactions: List[Dict[str, Any]]) -> CILMetric:
        """Calculate CIL metrics from interaction history"""
        # Initialize metric accumulators
        metric_scores = {
            'comprehension': [],
            'adaptation': [],
            'learning': [],
            'communication': [],
            'creativity': []
        }
        
        # Analyze each interaction
        for interaction in interactions:
            # Comprehension: How well the intelligence understands context
            if 'context_understanding' in interaction:
                metric_scores['comprehension'].append(
                    interaction['context_understanding'].get('score', 0)
                )
                
            # Adaptation: How well it adapts content
            if 'content_adaptation' in interaction:
                metric_scores['adaptation'].append(
                    interaction['content_adaptation'].get('effectiveness', 0)
                )
                
            # Learning: How much it learns from interactions
            if 'learning_progress' in interaction:
                metric_scores['learning'].append(
                    interaction['learning_progress'].get('improvement', 0)
                )
                
            # Communication: How effective its communication is
            if 'communication' in interaction:
                metric_scores['communication'].append(
                    interaction['communication'].get('clarity', 0)
                )
                
            # Creativity: How creative its solutions are
            if 'problem_solving' in interaction:
                metric_scores['creativity'].append(
                    interaction['problem_solving'].get('innovation', 0)
                )
        
        # Calculate average scores for each metric
        return CILMetric(
            comprehension=np.mean(metric_scores['comprehension']) if metric_scores['comprehension'] else 0,
            adaptation=np.mean(metric_scores['adaptation']) if metric_scores['adaptation'] else 0,
            learning=np.mean(metric_scores['learning']) if metric_scores['learning'] else 0,
            communication=np.mean(metric_scores['communication']) if metric_scores['communication'] else 0,
            creativity=np.mean(metric_scores['creativity']) if metric_scores['creativity'] else 0
        )
        
    def get_current_cil(self, intelligence_id: str) -> Optional[CILAssessment]:
        """Get the most recent CIL assessment for an intelligence"""
        if intelligence_id in self.assessments and self.assessments[intelligence_id]:
            return self.assessments[intelligence_id][-1]
        return None
        
    def get_cil_history(self, intelligence_id: str) -> List[CILAssessment]:
        """Get the complete CIL assessment history for an intelligence"""
        return self.assessments.get(intelligence_id, [])
        
    def save_assessments(self, file_path: str):
        """Save all CIL assessments to a file"""
        data = {
            'assessments': {
                int_id: [
                    {
                        'intelligence_id': a.intelligence_id,
                        'timestamp': a.timestamp.isoformat(),
                        'metrics': {
                            'comprehension': a.metrics.comprehension,
                            'adaptation': a.metrics.adaptation,
                            'learning': a.metrics.learning,
                            'communication': a.metrics.communication,
                            'creativity': a.metrics.creativity
                        },
                        'overall_score': a.overall_score,
                        'confidence': a.confidence,
                        'interaction_count': a.interaction_count
                    }
                    for a in assessments
                ]
                for int_id, assessments in self.assessments.items()
            }
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
            
    def load_assessments(self, file_path: str):
        """Load CIL assessments from a file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        self.assessments = {
            int_id: [
                CILAssessment(
                    intelligence_id=a['intelligence_id'],
                    timestamp=datetime.fromisoformat(a['timestamp']),
                    metrics=CILMetric(**a['metrics']),
                    overall_score=a['overall_score'],
                    confidence=a['confidence'],
                    interaction_count=a['interaction_count']
                )
                for a in assessments
            ]
            for int_id, assessments in data['assessments'].items()
        } 