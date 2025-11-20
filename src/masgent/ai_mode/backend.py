# masgent/ai_mode/backend.py

import os, sys
import asyncio
from dotenv import load_dotenv
from colorama import init, Fore, Style

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai import Agent

from masgent.ai_mode import tools

def ask_for_openai_api_key():
    key = input('Enter your OpenAI API key: ').strip()
    if not key:
        print('\nOpenAI API key cannot be empty. Exiting...\n')
        sys.exit(1)

    # Store temporarily for this session
    os.environ['OPENAI_API_KEY'] = key

    # Optional: write to .env so user never needs to type again
    save = input('\nSave this key to .env file for future? (y/n): ').strip().lower()
    if save == 'y':
        with open('.env', 'w') as f:
            f.write(f'OPENAI_API_KEY={key}\n')
        print('\nOpenAI API key saved to .env file.')
        
    print('\nOpenAI API key loaded.\n')

def ask_for_mp_api_key():
    key = input('Enter your Materials Project API key: ').strip()
    if not key:
        print('\nMaterials Project API key cannot be empty. Exiting...\n')
        sys.exit(1)

    # Store temporarily for this session
    os.environ['MP_API_KEY'] = key

    # Optional: write to .env so user never needs to type again
    save = input('\nSave this key to .env file for future? (y/n): ').strip().lower()
    if save == 'y':
        with open('.env', 'a') as f:
            f.write(f'MP_API_KEY={key}\n')
        print('\nMaterials Project API key saved to .env file.')
        
    print('\nMaterials Project API key loaded.\n')

def print_help():
    print('\nMasgent AI Mode usage:')
    print('  Chat with the AI by typing your questions or using specific commands.\n')
    print('Available commands:')
    print('  cli                → Switch to CLI mode')
    print('  help               → Show this help message')
    print('  exit               → Exit the program\n')

async def chat_stream(agent, user_input: str, history: list):
    async with agent.run_stream(
        user_prompt=user_input, 
        message_history=history
        ) as result:
        fully_reply = ''
        async for chunk in result.stream_text(delta=True):
            fully_reply += chunk
            print(Fore.CYAN + chunk + Style.RESET_ALL, end='', flush=True)
        print('\n')

        all_msgs = list(result.all_messages())
        
        return all_msgs

async def ai_mode(agent):
    history = []
    
    try:
        while True:
            user_input = input('Masgent AI > ').strip()

            if not user_input:
                continue
            
            if user_input in {'exit'}:
                return 'exit-mode'
            elif user_input in {'cli'}:
                return 'cli-mode'
            elif user_input in {'help'}:
                print_help()
            else:
                try:
                    history = await chat_stream(agent, user_input, history)
                    print(f'[Debug] Current conversation history length: {len(history)} messages.\n')
                except Exception as e:
                    print(f'[Error]: {e}')

    except (KeyboardInterrupt, EOFError):
        print('\nExiting Masgent. Goodbye!\n')
        sys.exit(0)

def main():
    load_dotenv(dotenv_path='.env')

    if 'OPENAI_API_KEY' not in os.environ:
        ask_for_openai_api_key()
    else:
        print('OpenAI API key found in environment.\n')

    if 'MP_API_KEY' not in os.environ:
        ask_for_mp_api_key()
    else:
        print('Materials Project API key found in environment.\n')

    model = OpenAIChatModel(model_name='gpt-5-nano')

    system_prompt = '''
You are MASGENT, a concise materials-simulation agent.

GENERAL RULES:
- Respond with ONE short sentence only.
- Never provide explanations unless the user asks.
- Never call a tool until ALL required parameters are completed and confirmed.

MISSING PARAMETER LOGIC:
- If any required parameter is missing, ask for ONLY ONE missing item at a time.
- Format: "Do you want to provide <natural-language description>, or should I decide for you?"
- Do NOT summarize all missing parameters at once.
- Only infer a parameter when the user explicitly says: "decide for me", "infer", "guess", or "you choose".

PARAMETER INFERENCE:
- Infer only ONE missing value per turn.
- Use typical crystallographic defaults when inferring.
- After inferring, continue asking for any remaining missing parameters.

FINAL CONFIRMATION:
- After ALL parameters are provided or inferred, ask:
  "Proceed using <summary of final parameters>?"
- Only run the tool when the user answers YES.

TOOL CALL RULES:
- Use a tool only when the user clearly requests an action the tool performs.
- After calling a tool, output ONLY the returned string.
- No extra commentary.

CLARITY:
- One short sentence only.
- No paragraphs.
- No multi-sentence replies.

    '''

    agent = Agent(
        model=model,
        system_prompt=system_prompt,
        tools=[
            tools.generate_vasp_poscar,
            tools.generate_vasp_inputs_from_poscar,
            tools.customize_vasp_kpoints_with_accuracy,
            tools.convert_structure_format,
            tools.convert_poscar_coordinates,
        ],
        )
    
    mode = asyncio.run(ai_mode(agent))
    return mode

if __name__ == '__main__':
    main()