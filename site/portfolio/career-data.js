const careerProjects = new Map([
  ['ai-workflows', {
    name: { zh: 'AI工程工作流', en: 'AI Engineering Workflows' },
    category: 'AI workflow engineering',
    url: null,
    tags: ['AI Workflows', 'Knowledge Engineering', 'Tool Integration', 'Automation'],
    kind: 'case',
    zh: {
      summary: '把运维知识、判断路径与执行工具组织起来，让 AI 工作流能够承接具体的工程任务。',
      context: '平台工程与日常运维自动化。',
      role: '主导工作流设计、知识整理与工具集成。',
      points: [
        '将领域经验整理为可复用的操作知识与提示词，明确任务目标和判断条件。',
        '把工具调用、执行检查与结果反馈连接起来，形成完整的工作流程。',
        '持续补充审查与排障案例，并通过分享和工具维护推动经验复用。'
      ],
      outcome: '沉淀了连接领域知识、执行工具与结果检查的工作流方法，让日常经验能够持续积累与复用。'
    },
    en: {
      summary: 'Organize operational knowledge, decision paths, and execution tools into AI workflows for concrete engineering tasks.',
      context: 'Platform engineering and everyday operations automation.',
      role: 'Led workflow design, knowledge organization, and tool integration.',
      points: [
        'Turned domain experience into reusable operational knowledge and prompts, with clear task objectives and decision criteria.',
        'Connected tool calls, execution checks, and result feedback into complete workflows.',
        'Expanded review and troubleshooting cases, and encouraged reuse through knowledge sharing and tool maintenance.'
      ],
      outcome: 'Established a workflow approach that connects domain knowledge, execution tools, and result checks, allowing everyday experience to accumulate and be reused.'
    }
  }],
  ['lifecycle', {
    name: { zh: '基础设施生命周期', en: 'Infrastructure Lifecycle' },
    category: 'Infrastructure lifecycle engineering',
    url: null,
    tags: ['GitOps', 'Infrastructure', 'Workflow Design', 'Automation'],
    kind: 'case',
    zh: {
      summary: '用平台化方式管理基础设施的创建、升级、扩容与退役，将分散操作组织为一致的生命周期流程。',
      context: '云基础设施与集群生命周期管理。',
      role: '主导平台方案设计与核心开发。',
      points: [
        '围绕生命周期阶段梳理操作边界，将共性需求组织为可复用的平台能力。',
        '通过声明式配置与 GitOps 工作流连接目标定义、变更审查和执行。',
        '统一不同生命周期操作的管理方式，让平台演进建立在共享流程之上。'
      ],
      outcome: '沉淀了可复用的生命周期管理能力，为基础设施变更提供一致的工程入口与流程。'
    },
    en: {
      summary: 'Manage infrastructure creation, upgrades, expansion, and retirement through a platform that brings separate operations into a consistent lifecycle.',
      context: 'Cloud infrastructure and cluster lifecycle management.',
      role: 'Led platform solution design and core development.',
      points: [
        'Defined operational boundaries around lifecycle stages and organized common requirements into reusable platform capabilities.',
        'Connected desired-state definitions, change reviews, and execution through declarative configuration and GitOps workflows.',
        'Unified the management of lifecycle operations so that platform evolution builds on shared processes.'
      ],
      outcome: 'Established reusable lifecycle management capabilities with a consistent engineering entry point and process for infrastructure changes.'
    }
  }],
  ['secure-delivery', {
    name: { zh: '安全基础制品交付', en: 'Secure Foundation Delivery' },
    category: 'Secure infrastructure delivery',
    url: null,
    tags: ['OS Hardening', 'Image Engineering', 'Security Patching', 'Automation'],
    kind: 'case',
    zh: {
      summary: '围绕操作系统镜像与中间件，将安全加固、自动化构建和补丁维护组织为持续交付能力。',
      context: '多云环境中的基础制品与安全维护。',
      role: '主导安全交付方案设计与自动化开发。',
      points: [
        '将操作系统与中间件的加固要求纳入标准化构建流程。',
        '梳理不同云环境的交付需求，以统一方法承接共性与差异。',
        '把上游安全更新、补丁整理与制品发布连接为可持续维护的流程。'
      ],
      outcome: '形成覆盖构建、加固与维护的基础制品交付能力，并将安全要求沉淀到可重复使用的工程流程中。'
    },
    en: {
      summary: 'Bring security hardening, automated builds, and patch maintenance together as continuous delivery capabilities for operating system images and middleware.',
      context: 'Foundation artifacts and security maintenance across cloud environments.',
      role: 'Led secure delivery solution design and automation development.',
      points: [
        'Incorporated operating system and middleware hardening requirements into standardized build processes.',
        'Organized delivery requirements across cloud environments, using a common approach for shared needs and differences.',
        'Connected upstream security updates, patch preparation, and artifact releases into a maintainable process.'
      ],
      outcome: 'Established foundation artifact delivery capabilities spanning builds, hardening, and maintenance, embedding security requirements in reusable engineering processes.'
    }
  }],
  ['platform-testing', {
    name: { zh: '平台测试与共享框架', en: 'Platform Testing & Shared Frameworks' },
    category: 'Platform automation and frameworks',
    url: null,
    tags: ['Python', 'Test Automation', 'Shared Frameworks', 'Platform Engineering'],
    kind: 'case',
    zh: {
      summary: '通过 Python 测试框架与共享工程能力，组织平台验证中的重复工作。',
      context: '平台自动化与测试验证。',
      role: '主导测试框架设计与开发，推动公共能力建设。',
      points: [
        '围绕平台验证需求开发 Python 自动化测试框架。',
        '把重复的执行逻辑与通用能力沉淀为公共库和共享框架。',
        '以统一的开发方式组织自动化流程，为不同测试场景提供可复用的基础。'
      ],
      outcome: '沉淀了测试执行与框架复用能力，让平台验证能够建立在共同的工程基础之上。'
    },
    en: {
      summary: 'Organize repetitive platform validation work through a Python testing framework and shared engineering capabilities.',
      context: 'Platform automation and test validation.',
      role: 'Led testing framework design and development, and advanced shared capabilities.',
      points: [
        'Developed a Python automation framework around platform validation needs.',
        'Extracted repetitive execution logic and common capabilities into shared libraries and frameworks.',
        'Organized automation through a consistent development approach, providing a reusable foundation for different testing scenarios.'
      ],
      outcome: 'Established testing execution and framework reuse capabilities so that platform validation can build on a common engineering foundation.'
    }
  }],
  ['service-health', {
    name: { zh: '服务健康与可观测性', en: 'Service Health & Observability' },
    category: 'Service assurance and observability',
    url: null,
    tags: ['Service Health', 'Observability', 'Distributed Checks', 'Automation'],
    kind: 'case',
    zh: {
      summary: '将分布式健康检查与服务状态检查组织为平台能力，为基础服务提供持续观察的视角。',
      context: '基础服务健康保障与状态检查。',
      role: '主导健康检查平台方案设计与开发。',
      points: [
        '围绕服务健康与状态需求，梳理可重复执行的检查内容。',
        '将分布式检查能力组织为共享平台，承接不同检查场景。',
        '结合服务状态与检查结果，为问题分析提供一致的观察入口。'
      ],
      outcome: '沉淀了分布式检查与服务状态观察能力，为日常健康保障和问题分析提供共同基础。'
    },
    en: {
      summary: 'Organize distributed health and service-state checks into platform capabilities for continuous visibility into foundation services.',
      context: 'Foundation service health assurance and state checks.',
      role: 'Led health-check platform solution design and development.',
      points: [
        'Defined repeatable checks around service health and state requirements.',
        'Organized distributed checking capabilities into a shared platform for different inspection scenarios.',
        'Brought service states and check results together as a consistent observation point for problem analysis.'
      ],
      outcome: 'Established distributed checking and service-state visibility capabilities, providing a common foundation for everyday health assurance and problem analysis.'
    }
  }],
  ['rolling-updates', {
    name: { zh: '服务更新与变更编排', en: 'Service Updates & Change Orchestration' },
    category: 'Update automation and orchestration',
    url: null,
    tags: ['Rolling Updates', 'Change Orchestration', 'Recovery', 'Automation'],
    kind: 'case',
    zh: {
      summary: '将服务更新、维护检查与失败恢复纳入共享流程，让日常变更具有一致的执行方式。',
      context: '基础服务更新与安全维护自动化。',
      role: '主导更新框架设计与自动化开发。',
      points: [
        '把服务更新与安全维护中的重复任务沉淀为共享更新能力。',
        '结合不同服务的状态需求，设计更新检查与变更编排方式。',
        '将失败恢复纳入框架设计，为维护流程提供可恢复的执行路径。'
      ],
      outcome: '形成可复用的更新与变更编排能力，将检查、执行和恢复组织为完整的维护流程。'
    },
    en: {
      summary: 'Bring service updates, maintenance checks, and failure recovery into shared processes for a consistent approach to everyday changes.',
      context: 'Foundation service updates and security maintenance automation.',
      role: 'Led update framework design and automation development.',
      points: [
        'Turned repetitive service update and security maintenance tasks into shared update capabilities.',
        'Designed update checks and change orchestration around the state requirements of different services.',
        'Incorporated failure recovery into the framework to provide recoverable execution paths for maintenance.'
      ],
      outcome: 'Established reusable update and change orchestration capabilities, bringing checks, execution, and recovery together as a complete maintenance process.'
    }
  }]
]);
