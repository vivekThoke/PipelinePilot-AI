from app.schemas.action import AgentAction

class ActionPolicy:
    """Deterministic safety policy for agent actions."""
    
    def requires_approval(
        self,
        action: AgentAction
    ) -> bool:
        """Determines wheather an action requires approval."""
        
        if action.action_type == "update_lead_status":
            return True
        
        if action.action_type == "create_follow_up_task":
            if action.priority == "high":
                return True
            
            return False
        
        return True