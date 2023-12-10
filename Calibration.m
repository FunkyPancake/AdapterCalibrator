% Calibrate adapter board 
% return linear function coeficient y = [a] * x + [b]
function [a,b] = Calibrate()
    calTime = 5;
    calPointLow = 1.0;
    calPointHigh = 4;
    deviceList = daqlist("ni");
    
    if(isempty(deviceList))
        error("Device not connected.");
    end
    
    id = d{1,"DeviceID"};
    dq = daq("ni");
    
    chVinSignalIn = addinput(dq,id,"ai0","Voltage");
    chVinSignalIn.Range = [-5 5];

    chVinSignalRef = addinput(dq,id,"ai1","Voltage");
    chVinSignalRef.Range = [-5 5];

    chVinSupply = addinput(dq,id,"ai2","Voltage");
    chVinSupply.Range = [-5 5];

    chBoardDetected = addinput(dq,id,"Port0/Line0","Digital");

    chVoutSignalRef = addoutput(dq,id,"ao0","Voltage");
    chVoutSignalRef.Range = [-5 5];
    
    chLedInProgress = addoutput(dq,id,"Port0/Line1","Digital");
    chLedDone = addoutput(dq,id,"Port0/Line2","Digital");

    trigger = addtrigger(dq, 'Digital','StartTrigger',chBoardDetected,)

    start(dq,"Duration",calTime);
    write(dq,[decimalToBinaryVector(2),calPointLow]);

    write(chLedInProgress,1);
    write(chLedDone,0);


    stop(dq)
end