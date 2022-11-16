param ($port)

echo "hai"
echo $port

$foundProcesses = netstat -ano | findstr :$port
echo $foundProcesses 
$activePortPattern = ":$port\s.+LISTENING\s+\d+$"
$pidNumberPattern = "\d+$"

echo $pidNumberPattern
IF ($foundProcesses | Select-String -Pattern $activePortPattern -Quiet) {
	echo "we are in if loop"
  $matches = $foundProcesses | Select-String -Pattern $activePortPattern
  $firstMatch = $matches.Matches.Get(0).Value

  $pidNumber = [regex]::match($firstMatch, $pidNumberPattern).Value

  taskkill /pid $pidNumber /f
}