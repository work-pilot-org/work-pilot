import asyncio
from modules.hr.tool_definitions import get_hr_tool_definitions
from google import genai
from google.genai import types
from shared_infrastructure.core.config import settings

async def main():
    tools = get_hr_tool_definitions()
    client = genai.Client(api_key=settings.gemini_api_key)
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text="Allocate 10 days of SICK leave to all employees for the year 2026.")],
        )
    ]
    
    config = types.GenerateContentConfig(
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True,
        ),
    )
    
    try:
        print("Sending request with tools using gemini-1.5-flash...")
        res = await client.aio.models.generate_content(
            model="gemini-1.5-flash",
            contents=contents,
            config=config
        )
        print("Success!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        if hasattr(e, 'code'):
            print("Code:", e.code)
        if hasattr(e, 'message'):
            print("Message:", e.message)
        if hasattr(e, 'details'):
            print("Details:", e.details)

if __name__ == "__main__":
    asyncio.run(main())
