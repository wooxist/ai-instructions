# 11장. 인스트럭션 시스템을 위한 도구와 프레임워크

**Part 3: 인스트럭션 시스템의 확장과 운영**

**목적:** 에이전트가 실제 세상과 상호작용하고, 인스트럭션 시스템을 효율적으로 관리하며, 그 미래를 조망하는 데 도움이 되는 다양한 도구, 프레임워크, 표준을 이해합니다.

### 이 장에서 배우는 것
- 에이전트에게 '손과 발'을 달아주는 도구의 역할과 종류.
- 에이전트가 도구를 사용하게 만드는 '도구 명세' 설계 방법.
- 에이전트 구축, 관리, 평가를 위한 주요 프레임워크와 서비스.
- 도구 사용의 위험성과 안전장치.
- 파편화된 현재를 넘어, 표준 프로토콜(MCP)을 통한 상호운용성의 미래.

---

## 들어가며: 왜 도구가 필요한가?

지금까지 우리가 설계한 에이전트는 명확한 역할과 지시를 따르는 똑똑한 '뇌'와 같습니다. 하지만 이 뇌가 아무리 뛰어나도, 외부 세계와 상호작용할 '손과 발'이 없다면 그 능력은 텍스트를 생성하는 데 그칩니다. **도구(Tool)**는 바로 이 에이전트에게 손과 발을 달아주는 역할을 합니다.

도구를 통해 에이전트는 단순히 정보를 처리하는 것을 넘어, 실시간으로 웹을 검색하고, 데이터베이스에서 정보를 가져오고, 코드를 실행하여 복잡한 계산을 수행하며, 다른 서비스의 API를 호출하여 이메일을 보내거나 프로젝트 관리 도구에 티켓을 생성할 수 있습니다. 즉, 도구는 에이전트를 단순한 챗봇에서 실제 업무를 수행하는 강력한 **자동화 엔진**으로 변모시키는 핵심 요소입니다.

## 11.1 도구의 종류와 역할

도구는 특정 제품이나 라이브러리의 이름이 아니라, 에이전트가 수행하는 '기능'을 중심으로 분류할 수 있습니다. 이는 기술 변화에 상관없이 도구의 본질을 이해하는 데 도움이 됩니다.

- **정보 수집 도구 (Information Gathering Tools):** 에이전트가 답변을 생성하는 데 필요한 정보를 외부에서 가져오는 역할을 합니다.
  - **웹 검색 (Web Search):** 최신 뉴스, 시장 동향 등 실시간 공개 정보를 수집합니다.
  - **파일 시스템 접근 (File System Access):** 로컬 또는 원격 저장소의 파일을 읽거나 쓰는 작업을 수행합니다.
  - **데이터베이스 조회 (Database Query):** SQL 등을 사용하여 정형 데이터베이스에서 필요한 정보를 직접 조회합니다.

- **코드 실행 도구 (Code Execution Tools):** 에이전트가 언어 모델만으로는 수행하기 어려운 복잡한 논리, 계산, 데이터 조작을 수행하게 합니다.
  - **Python/JavaScript 인터프리터:** 통계 계산, 데이터 시각화, 알고리즘 실행 등 코드의 힘을 빌려 문제를 해결합니다.

- **외부 서비스 연동 도구 (External Service Integration Tools):** 다른 소프트웨어나 서비스의 기능을 호출하여 작업의 범위를 무한히 확장합니다.
  - **API 호출 (API Calls):** Gmail API로 이메일을 보내거나, Jira API로 이슈를 생성하고, Slack API로 팀 채널에 메시지를 보내는 등 다른 서비스와 연동하여 실제 업무를 자동화합니다.

## 11.2 에이전트에게 도구를 부여하는 방법

에이전트가 도구를 스스로 판단하여 사용하게 하려면, 각 도구의 '사용 설명서'를 명확하게 작성해주어야 합니다. 이를 **도구 명세(Tool Specification)**라고 하며, 일반적으로 다음과 같은 요소로 구성됩니다.

- **`tool_name` (도구 이름):** `web_search`, `execute_python_code` 와 같이 고유하고 명확한 이름을 부여합니다.
- **`description` (설명):** **(가장 중요)** 에이전트(LLM)가 이 도구를 '언제' 사용해야 하는지를 자연어로 명확하게 설명합니다. 예를 들어, "최신 정보나 실시간 이벤트에 대한 질문에 답해야 할 때 이 도구를 사용하세요." 와 같이 구체적인 사용 사례를 제시해야 합니다.
- **`input_schema` (입력 스키마):** 도구를 사용하는 데 필요한 파라미터들의 이름, 데이터 타입, 설명을 JSON Schema 형식으로 정의합니다.
- **`output_schema` (출력 스키마):** 도구가 실행된 후 반환하는 결과물의 데이터 구조를 JSON Schema 형식으로 정의합니다.

#### 예시: 웹 검색 도구 정의
```json
{
  "name": "web_search",
  "description": "최신 정보나 특정 주제에 대한 실시간 정보가 필요할 때 인터넷을 검색하는 도구입니다.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "검색할 키워드나 질문"
      }
    },
    "required": ["query"]
  }
}
```

## 11.3 주요 프레임워크와 서비스

앞서 설명한 개념들을 실제 환경에서 더 쉽게 구축하고 관리할 수 있도록 돕는 다양한 도구들이 있습니다.

### 11.3.1 에이전트 구축 프레임워크
- **LangChain, LlamaIndex:** 이들은 LLM을 외부 데이터 소스나 도구와 쉽게 연결할 수 있도록 돕는 대표적인 오픈소스 라이브러리입니다. 복잡한 에이전트 실행 루프, 메모리 관리, 워크플로우(Chain) 구성 등 7장에서 다룬 개념들을 코드로 구현하는 데 필수적인 프레임워크 역할을 합니다.

### 11.3.2 인스트럭션 관리 및 버전 관리
- **GitHub:** 10장에서 설계한 파일 기반 인스트럭션 시스템의 버전 관리에 가장 이상적인 도구입니다. `main.md`, `agents/`, `schemas/` 등의 변경 이력을 추적하고, 팀원들과 협업하여 인스트럭션을 개선할 수 있습니다.
- **Notion, Obsidian:** 개인이나 소규모 팀의 인스트럭션(프롬프트)을 저장하고 관리하는 지식 관리 도구로 유용합니다. 특히 자주 사용하는 인스트럭션 조각들을 템플릿으로 만들어 쉽게 재사용할 수 있습니다.

### 11.3.3 성능 평가 및 모니터링
- **LangSmith, Weights & Biases (W&B), PromptLayer:** 이와 같은 LLMOps(대규모 언어 모델 운영) 도구들은 에이전트와 사용자의 모든 상호작용을 로그로 기록하고, 각 단계의 비용, 지연 시간, 성공률 등을 추적하여 성능 병목을 찾아내는 데 도움을 줍니다. 복잡한 워크플로우를 디버깅하고 개선하는 데 필수적입니다.

## 11.4 도구 사용의 위험성과 안전장치

에이전트에게 도구를 부여하는 것은 강력한 힘을 주는 동시에 큰 책임과 위험을 수반합니다. 특히 파일 시스템을 수정하거나, 코드를 실행하거나, 외부로 데이터를 전송하는 도구는 신중하게 다루어야 합니다.

- **보안 위험:** 프롬프트 인젝션 공격으로 인해 에이전트가 악성 코드를 실행하거나, 로컬 파일을 삭제하거나, 민감한 정보를 외부로 유출할 수 있습니다.

이러한 위험을 통제하기 위해, 우리는 4장에서 배운 **검증 및 책임 원칙**들을 바탕으로 다음과 같은 안전장치를 반드시 마련해야 합니다.

- **최소 권한 원칙 (Principle of Least Privilege):** 에이전트에게는 작업을 수행하는 데 꼭 필요한 최소한의 도구와 권한만을 부여해야 합니다.
- **인간의 승인 (Human-in-the-Loop):** 되돌릴 수 없거나 중요한 작업을 수행하기 전에는, 반드시 인간 사용자의 최종 승인을 받도록 워크플로우를 설계해야 합니다.
- **샌드박싱 (Sandboxing):** 코드를 실행할 때는 Docker 컨테이너와 같은 격리된 '샌드박스' 환경에서 실행하여, 시스템에 미치는 영향을 원천적으로 차단해야 합니다.

## 11.5 MCP: 상호운용성을 위한 표준 프로토콜

현재의 에이전트와 도구 생태계는 매우 파편화되어 있습니다. OpenAI, Google, Anthropic 등 각 모델 제공사들은 저마다 다른 방식으로 도구를 정의하고 호출합니다. 이는 개발자들이 특정 플랫폼에 종속되게 만들고, 서로 다른 시스템의 에이전트들이 협력하는 것을 거의 불가능하게 만듭니다.

이러한 문제를 해결하기 위한 노력으로, **MCP(Model-Context Protocol)**라는 표준 프로토콜이 등장했습니다. MCP는 인간, AI 모델, 도구가 서로의 역할, 기능, 맥락을 이해하고 소통하기 위한 '공용어(Lingua Franca)'를 지향합니다. 이는 마치 전 세계의 컴퓨터가 HTTP라는 프로토콜 위에서 소통하며 월드 와이드 웹을 이룬 것과 같습니다. 최근 일부 업체들이 MCP를 지원하는 서버를 출시하기 시작하면서, 이는 더 이상 가상의 개념이 아닌 현실적인 표준으로 자리잡아가고 있습니다.

## 참고 자료

- Anthropic. (2023). Claude Function Calling. https://docs.anthropic.com/claude/docs/function-calling
- Hohpe, G., & Woolf, B. (2003). *Enterprise Integration Patterns*. Addison-Wesley Professional.
- Langchain Documentation. (2023). https://docs.langchain.com/
- LlamaIndex Documentation. (2023). https://www.llamaindex.ai/
- OpenAI. (2023). Function Calling. https://platform.openai.com/docs/guides/function-calling
- PromptLayer Documentation. (2023). https://promptlayer.com/docs
- Weights & Biases Documentation. (2023). https://docs.wandb.ai/
� 에이전트들을 동적으로 찾아, 스스로 팀을 구성하고 워크플로우를 설계하여 복잡한 문제를 해결하게 될 것입니다.

## 참고 자료

- Anthropic. (2023). Claude Function Calling. https://docs.anthropic.com/claude/docs/function-calling
- Hohpe, G., & Woolf, B. (2003). *Enterprise Integration Patterns*. Addison-Wesley Professional.
- Langchain Documentation. (2023). https://docs.langchain.com/
- LlamaIndex Documentation. (2023). https://www.llamaindex.ai/
- OpenAI. (2023). Function Calling. https://platform.openai.com/docs/guides/function-calling
- PromptLayer Documentation. (2023). https://promptlayer.com/docs
- Weights & Biases Documentation. (2023). https://docs.wandb.ai/
