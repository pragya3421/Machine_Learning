%% https://www.mathworks.com/matlabcentral/fileexchange/46035-confusionmatstats-group-grouphat

function [ClassPerformance, OverallAccuracy] = CFM_Stats(group,grouphat) % edit by Dr. Lai
% INPUT
% group = true class labels
% grouphat = predicted class labels
%
% OR INPUT
% stats = confusionmatStats(group);
% group = confusion matrix from matlab function (confusionmat)
%
% OUTPUT
% stats is a structure array
% stats.confusionMat
%               Predicted Classes
%                    p'    n'
%              ___|_____|_____| 
%       Actual  p |     |     |
%      Classes  n |     |     |
%
% stats.accuracy = (TP + TN)/(TP + FP + FN + TN) ; the average accuracy is returned
% stats.precision = TP / (TP + FP)                  % for each class label
% stats.sensitivity = TP / (TP + FN)                % for each class label
% stats.specificity = TN / (FP + TN)                % for each class label
% stats.recall = sensitivity                        % for each class label
% stats.Fscore = 2*TP /(2*TP + FP + FN)            % for each class label
%
% TP: true positive, TN: true negative, 
% FP: false positive, FN: false negative
% 

field1 = 'confusionMat';
if nargin < 2
    value1 = group;
else
    [value1,gorder] = confusionmat(group,grouphat);
end

numOfClasses = size(value1,1);
totalSamples = sum(sum(value1));

[TP,TN,FP,FN,accuracy,sensitivity,specificity,precision,f_score] = deal(zeros(numOfClasses,1));
for class = 1:numOfClasses
   TP(class) = value1(class,class);
   tempMat = value1;
   tempMat(:,class) = []; % remove column
   tempMat(class,:) = []; % remove row
   TN(class) = sum(sum(tempMat));
   FP(class) = sum(value1(:,class))-TP(class);
   FN(class) = sum(value1(class,:))-TP(class);
end

for class = 1:numOfClasses
    accuracy(class) = (TP(class) + TN(class)) / totalSamples;
    sensitivity(class) = TP(class) / (TP(class) + FN(class));
    specificity(class) = TN(class) / (FP(class) + TN(class));
    precision(class) = TP(class) / (TP(class) + FP(class));
    f_score(class) = 2*TP(class)/(2*TP(class) + FP(class) + FN(class));
end

field2 = 'accuracy';  value2 = accuracy;
field3 = 'sensitivity';  value3 = sensitivity;
field4 = 'specificity';  value4 = specificity;
field5 = 'precision';  value5 = precision;
field6 = 'recall';  value6 = sensitivity;
field7 = 'Fscore';  value7 = f_score;
stats = struct(field1,value1,field2,value2,field3,value3,field4,value4,field5,value5,field6,value6,field7,value7);
%{
if exist('gorder','var')
    stats = struct(field1,value1,field2,value2,field3,value3,field4,value4,field5,value5,field6,value6,field7,value7,'groupOrder',gorder);
end
%}
%% added by Dr. Chih Lai
disp('Confusion Matrix:')
disp(stats(1).confusionMat), %disp(' ')
OverallAccuracy = sum(diag(stats(1).confusionMat)) / (sum(sum(stats(1).confusionMat)));
disp(['Overall accuracy = ' num2str(OverallAccuracy)])


for class = 1 : numOfClasses
    %ClassPerformance(class).groupOrder = stats(1).groupOrder(class);
    ClassPerformance(class).accuracy = stats(1).accuracy(class);
    ClassPerformance(class).precision = stats(1).precision(class);
    ClassPerformance(class).recall = stats(1).recall(class);
    ClassPerformance(class).Fscore = stats(1).Fscore(class);
    ClassPerformance(class).sensitivity = stats(1).sensitivity(class);
    ClassPerformance(class).specificity = stats(1).specificity(class);
end
ClassPerformance = struct2table(ClassPerformance);
    