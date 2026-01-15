"""
Structure generation tools for SmartThings MCP Server.
These tools allow LLMs to generate validated structured outputs by calling tools
instead of generating JSON text.
"""
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


def register_tools(mcp):
    """
    Register structure generation tools with the MCP server.
    
    Args:
        mcp: FastMCP server instance
    """
    
    @mcp.tool()
    def generate_context_analysis(
        intent: str,
        entities: List[Dict[str, Any]],
        ambiguities: List[Dict[str, Any]] = None,
        reasoning: str = "",
        confidence: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate structured context analysis for user queries.
        
        The LLM calls this tool to create a validated context analysis structure
        instead of generating JSON text (which is error-prone with small models).
        
        Args:
            intent: User's intent - must be one of: "query", "control", "status", "other"
            entities: List of extracted entities, each with:
                - type: Entity type (action, device, room, location, capability, state)
                - value: The extracted value
                - confidence: Confidence score 0.0-1.0
                - metadata: Optional dict with additional context
            ambiguities: List of identified ambiguities (optional), each with:
                - description: What is ambiguous
                - options: List of possible interpretations
                - requires_user_input: Whether user clarification is needed
                - resolution_strategy: How to resolve automatically
            reasoning: LLM's reasoning about the classification
            confidence: Overall confidence in the analysis (0.0-1.0)
            
        Returns:
            Validated context analysis structure
            
        Example:
            generate_context_analysis(
                intent="query",
                entities=[
                    {"type": "action", "value": "list", "confidence": 1.0, "metadata": {}},
                    {"type": "capability", "value": "device", "confidence": 1.0, "metadata": {}}
                ],
                ambiguities=[],
                reasoning="Clear query to list all devices",
                confidence=1.0
            )
        """
        # Validate intent
        valid_intents = ["query", "control", "status", "other"]
        if intent not in valid_intents:
            logger.warning(f"Invalid intent '{intent}', defaulting to 'other'")
            intent = "other"
        
        # Validate confidence
        confidence = max(0.0, min(1.0, confidence))
        
        # Ensure ambiguities is a list
        if ambiguities is None:
            ambiguities = []
        
        # Validate entities
        validated_entities = []
        for entity in entities:
            if not isinstance(entity, dict):
                logger.warning(f"Skipping invalid entity: {entity}")
                continue
            
            # Ensure required fields
            if "type" not in entity or "value" not in entity:
                logger.warning(f"Entity missing type or value: {entity}")
                continue
            
            # Add defaults
            validated_entity = {
                "type": str(entity["type"]),
                "value": str(entity["value"]),
                "confidence": float(entity.get("confidence", 0.5)),
                "metadata": entity.get("metadata", {})
            }
            validated_entities.append(validated_entity)
        
        result = {
            "intent": intent,
            "entities": validated_entities,
            "ambiguities": ambiguities,
            "reasoning": reasoning,
            "confidence": confidence
        }
        
        logger.info(f"✓ Generated context analysis: intent={intent}, entities={len(validated_entities)}")
        
        return result
    
    @mcp.tool()
    def generate_execution_plan(
        tool_calls: List[Dict[str, Any]],
        reasoning: str = "",
        requires_user_input: bool = False,
        user_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured execution plan for SmartThings operations.
        
        The LLM calls this tool to create a validated execution plan structure
        instead of generating JSON text.
        
        Args:
            tool_calls: List of tools to call in sequence, each with:
                - tool_name: Name of the tool to call
                - parameters: Dict of parameters for the tool
                - description: What this tool call does
            reasoning: Why this plan will work
            requires_user_input: Whether user clarification is needed
            user_prompt: Prompt to show user if input required
            
        Returns:
            Validated execution plan structure
            
        Example:
            generate_execution_plan(
                tool_calls=[
                    {
                        "tool_name": "list_locations",
                        "parameters": {},
                        "description": "Get all locations"
                    },
                    {
                        "tool_name": "list_devices",
                        "parameters": {"location_id": "USE_FIRST_LOCATION_FROM_PREVIOUS_RESULT"},
                        "description": "List all devices in the location"
                    }
                ],
                reasoning="Need location first, then can list devices",
                requires_user_input=False
            )
        """
        # Validate tool calls
        validated_calls = []
        for tool_call in tool_calls:
            if not isinstance(tool_call, dict):
                logger.warning(f"Skipping invalid tool call: {tool_call}")
                continue
            
            # Ensure required fields
            if "tool_name" not in tool_call:
                logger.warning(f"Tool call missing tool_name: {tool_call}")
                continue
            
            validated_call = {
                "tool_name": str(tool_call["tool_name"]),
                "parameters": tool_call.get("parameters", {}),
                "description": str(tool_call.get("description", ""))
            }
            validated_calls.append(validated_call)
        
        result = {
            "plan": validated_calls,
            "reasoning": reasoning,
            "requires_user_input": requires_user_input,
            "user_prompt": user_prompt
        }
        
        logger.info(f"✓ Generated execution plan: {len(validated_calls)} tool calls")
        
        return result
    
    logger.info("Registered structure generation tools: generate_context_analysis, generate_execution_plan")
