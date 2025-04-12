
import re
import subprocess
import time
from metagpt.llm import LLM
from metagpt.actions import Action, UserRequirement
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.logs import logger
from metagpt.team import Team
from metagpt.context import Context
from metagpt.environment import Environment

def parse_code(rsp):
    pattern = r'```python(.*)```'
    match = re.search(pattern, rsp, re.DOTALL)
    code_text = match.group(1) if match else rsp
    return code_text

    
class DesigneCode(Action):

    PROMPT_TEMPLATE: str = """
    **Context**:
    Based on the code analysis provided by the Analyst, your task is to design a new and interesting bullet pattern or ability for the player's plane that can be smoothly integrated into the game.
    Ensure the ability is feasible within the current architecture and does not exceed 100 words in the description.
    **Tasks**:
    - Propose one new bullet pattern or ability for the player's plane.
    - Provide a detailed description of the ability.
    - Explain how this ability enhances gameplay and offers a unique experience.
    - Describe how it fits into the existing code structure and how it can be implemented.

    **Guidelines**:
    - Ensure the proposed ability is feasible within the current architecture.
    - Consider the impact on game balance and player enjoyment.
    - Do not write any code; focus on the design and integration aspects.

    **Code **:
    {code}
    """

    name: str = "DesigneCode"

    async def run(self, code: str):
        prompt = self.PROMPT_TEMPLATE.format(code=code)

        rsp = await self._aask(prompt)

        code_text = parse_code(rsp)
        return code_text


class designer(Role):

    name: str = "Alice"
    profile: str = "design new bullet"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([DesigneCode])

    
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        with open('bullet_metagpt.py', 'r', encoding='utf-8') as file:
            code = file.read()
        msg = Message(content=code, role=self.profile, send_to=coder)
        code = await todo.run(code)

        msg = Message(content=code, role=self.profile, cause_by=type(todo))

        return msg


class WriteCode(Action):
    
    PROMPT_TEMPLATE :str = """
    **Context**:
    Using the design provided by the Designer and Code, IMPORTANT:your task is to implement the new bullet pattern or ability in the Bullet class based on buff_num2. 
    The response should contain only the complete code for each section (`bullet.py`, `buff1`, and `buff2`), with no additional text or explanation.
    
    **Tasks**:
    - Write the code to implement the new bullet pattern or ability.
    - Integrate the new code with the existing classes and methods in `bullet.py`.
    - Ensure the new code follows the project's coding standards and conventions.

    **Guidelines**:
    - Write clean, readable, and well-documented code.
    - Use appropriate design patterns if applicable.
    - Do not alter existing functionality unless necessary for integration.
    - Test the new code to ensure it functions correctly within the game.

    **Design Information**:
    {design_text}

    **Code **:
    {code}

    """
    name: str = "WriteCode" 

    async def run(self, design_text:str,code:str):
        prompt = self.PROMPT_TEMPLATE.format(design_text=design_text, code=code)

        rsp = await self._aask(prompt)

        code_text = parse_code(rsp)
        return code_text


class coder(Role):

    name: str = "Bob"
    profile: str = "Generate new powerup code"
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([WriteCode])
        self._watch([DesigneCode])

    async def _act(self) -> Message:

        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        design_text = self.rc.memory.get_by_action(DesigneCode)
        with open('bullet_metagpt.py', 'r', encoding='utf-8') as file:
            code = file.read()

        logger.info(f"design_text: {design_text}")

        code = await todo.run(design_text, code)
        
        with open('bullet.py', 'w') as f:
            f.write(code)
        with open('bullet1.py', 'w') as f:
            f.write(code)   
        logger.info("Generated code saved to 'update_bullet.py'.")
        msg = Message(content=code, role=self.profile, cause_by=type(todo))

        return msg
    
    
class RunCode(Action):
    name: str = "Read_code"

    async def run(self):
        script_path = r"./plane_main.py"
        try:
                process = subprocess.run(
                ['python', script_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30
    )

                return process.stdout, process.stderr 

        except Exception as e:

                return None, str(e) 


class ModifyCode(Action):

    PROMPT_TEMPLATE: str = """
    **Context**:
    I am developing a plane game and encountered an error when running the `bullet.py` code using `subprocess.run` in Python. 
    The error message is shown below. I need your assistance to modify the `bullet.py` code to fix the issue based on the error details.

    **Error Details**:
    {context}
    **code**
    {generated_code}
    **Task**:
    1. Analyze the error message above and identify the part of the code in `bullet.py` that needs modification.
    2. Provide the **entire modified code** of `bullet.py` with the corrections implemented.
    3. Highlight the specific changes you made in a separate section, explaining why the modifications were necessary and how they fix the issue.

    **Guidelines**:
    - Ensure the modified code maintains the coding standards and conventions used in the original `bullet.py`.
    - Test the modified code in your environment to verify that it works as expected without errors before returning the result.
    - Return both the **full modified code** and the **explanation of changes** in your response.
    """

    name: str = "ModifyCode"
    async def run(self, context: str, generated_code: str):
        prompt = self.PROMPT_TEMPLATE.format(context=context,generated_code=generated_code)

        rsp = await self._aask(prompt)

        code_text = parse_code(rsp)

        return code_text


class checker(Role):

    name: str = "Rita"
    profile: str = "run code, if error modifyCode"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([RunCode,ModifyCode])
        self._watch([WriteCode])
        self._set_react_mode(react_mode="by_order")

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        if isinstance(todo,RunCode):
            
            stdout, stderr= await todo.run()
            logger.info(f"stdout:{stdout}")
            if stderr:
                msg= Message(content=f"stderr:{stderr}", role=self.profile, cause_by=type(todo))
            else:
                msg= Message(content=f"stdout:{stdout}", role=self.profile, cause_by=type(todo))
            
            return msg

        else:
            text = Message(sent_from=RunCode)
            logger.info(f"text:{text}")
            with open('bullet.py', 'r', encoding='utf-8') as file:
                code = file.read()
            code = await todo.run(text,code)
            with open('bullet.py', 'w') as f:
                f.write(code)
            logger.info("Generated code saved to 'Plane_Game/bullet.py'.")
            msg = Message(content=code, role=self.profile, cause_by=type(todo))
        
            return msg
        

class AnaylsisOutput(Action):
    PROMPT_TEMPLATE: str = """
    **Context**:
    Based on the description of the output and design text, propose suggestions for the next bullet upgrades. 
    The output is a list, such as [0, 1, 0, 1], where each position in the list represents a direction: 
    0 indicates left, 1 indicates right, 2 indicates up, and 3 indicates down. 
    Please provide specific upgrade plans based on this information.
    
    **design_text**:
    {design_text}
    **output**
    {output}
     """
    name: str = "Analysis output"

    async def run(self, output: str, design_text: str):
        prompt = self.PROMPT_TEMPLATE.format(output=output,design_text=design_text)

        rsp = await self._aask(prompt)

        code_text = parse_code(rsp)

        return code_text
    
    
class UpdateCode(Action):  
    PROMPT_TEMPLATE: str = """
    **Context**:
    Generate code that upgrades `buff2` in the `player_fire` method to make it stronger as `buff2_num` increases, 
    similar to the functionality of `buff1`. Ensure that `buff2` enhances its effects based on the value of `buff2_num`. Max color number is 3.
    Include all necessary code for `bullet`, `buff1`, and `buff2` without any descriptive text or explanations.
    **code**
    {generated_code}
    **upgrade plans**
    {output}
    """  
    name: str = "UpdateCode"
    async def run(self, output: str, generated_code: str):

        prompt = self.PROMPT_TEMPLATE.format(output=output,generated_code=generated_code)

        rsp = await self._aask(prompt)

        code_text = parse_code(rsp)

        return code_text
    
class updater(Role):

    name: str = "Leo"
    profile: str = "Analysis original bullet and update new bullet"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AnaylsisOutput,UpdateCode])
        self._watch([DesigneCode,WriteCode])
        

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        if isinstance(todo,AnaylsisOutput):

            design_text = Message(sent_from = DesigneCode)
            output = Message(sent_from=RunCode)

            code_text = await todo.run(output.content,design_text.content)

            logger.info(f"Analysis: {output})")

            msg = Message(content=code_text, role=self.profile, cause_by=type(todo))
        else:
            output = Message(sent_from=AnaylsisOutput)

            with open('bullet.py', 'r', encoding='utf-8') as file:
                code = file.read()

            code_text = await todo.run(output.content,code)

            msg = Message(content=code_text, role=self.profile, cause_by=type(todo))

        return msg
    
async def main(idea: str = "bullet_metagpt.py"):
    """
    logger.info(idea)
    team = Team()
    team.hire(
        [
            analyst(),
            designer(),
            coder(),
 
        ]
        #          
            
    )
    #team.run_project(idea)
    #await team.run()
    """
    context = Context() 
    env = Environment(context=context)
    env.add_roles([designer(), coder(), checker(),updater()])
    env.publish_message(Message(content=idea, send_to=designer)) 
    while not env.is_idle: 
        await env.run()

await main("Complete design, writing, running, checking, modifications, analysis and updates.If an error occurs during the run, the modified code must be run again afterward. ")