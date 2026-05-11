
path = 'octogent/dist/web/assets/index-CtEbQR-f.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Suavização (1.6s para um ciclo mais calmo e elegante)
content = content.replace('dur:"1.0s"', 'dur:"1.6s"')
# Ajustando o intervalo de saída para 0.25s (perfeito para 5 pontos em 1.6s)
content = content.replace('begin:`${o*.15}s`', 'begin:`${o*.25}s`')

# 2. Mantendo o Brilho e Tamanho Premium
# (Já aplicado no patch anterior, mas garantindo que persista)
content = content.replace('r:5.5', 'r:7.0')
content = content.replace('r:3.8', 'r:4.2')
content = content.replace('drop-shadow(0 0 4px', 'drop-shadow(0 0 10px')

# 3. Mantendo a Conexão Maestro e Sensibilidade
content = content.replace('state!=="idle"', 'state!=="finished"')
import re
if 'source:(f!=="orchestrator"?"t:orchestrator":m)' not in content:
    content = content.replace('source:m,target:buildTentacleNodeId(f)', 'source:(f!=="orchestrator"?"t:orchestrator":m),target:buildTentacleNodeId(f)')

# 4. Halo de Processamento
halo_code = '(h||a.agentRuntimeState==="processing")&&c.jsx("circle",{className:"canvas-node-focus-glow "+(a.agentRuntimeState==="processing"?"canvas-node-processing-halo":""),r:a.radius+(a.agentRuntimeState==="processing"?20:-4),fill:D,opacity:a.agentRuntimeState==="processing"?.7:1})'
if 'canvas-node-processing-halo' not in content:
    content = content.replace('h&&c.jsx("circle",{className:"canvas-node-focus-glow",r:a.radius-4,fill:D})', halo_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch 'Premium Smooth' aplicado com sucesso!")
