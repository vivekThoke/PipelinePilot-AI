from app.schemas.action import AgentAction
from app.tools.crm_tools import CRMTools

class AgentActionExecutor:
    """Executes approved agent actions."""
    
    def __init__(
        self,
        crm_tools: CRMTools
    ) -> None:
        self.crm_tools = crm_tools
        
    async def execute(
        self,
        action: AgentAction,
    ) -> dict[str, object]:
        """Executes a validated action."""
        
        if action.action_type == (
            "create_follow_up_task"
        ): 
            if action.title is None:
                raise ValueError(
                    "Task title is required"
                )
                
            return await (
                self.crm_tools
                .create_follow_up_task(
                    lead_id=action.lead_id,
                    title=action.title,
                    description=action.description,
                    priority=action.priority
                )
            )
            
        if action.action_type == (
            "update_lead_status"
        ): 
            if action.new_status is None:
                raise ValueError(
                    "New status is required"
                )
                
            return await (
                self.crm_tools
                .update_lead_status(
                    lead_id=action.lead_id,
                    status=action.new_status
                )
            )
        
        raise ValueError(
            f"Unsupported action: "
            f"{action.action_type}"
        )