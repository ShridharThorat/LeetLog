class SpreadsheetHelper {
  constructor(sheet) {
    this.sheet = sheet;
    this.ui = SpreadsheetApp.getUi();
  }

  static getActiveSheet() {
    return new SpreadsheetHelper(SpreadsheetApp.getActiveSheet());
  }

  getNamedRange(rangeName) {
    return this.sheet.getRange(rangeName);
  }

  showAlert(title, message) {
    this.ui.alert(title, message, this.ui.ButtonSet.OK);
  }
}

class TableProcessor {
  constructor(sheetHelper, rangeName) {
    this.sheetHelper = sheetHelper;
    this.range = sheetHelper.getNamedRange(rangeName);
    this.headers = this.range.offset(0, 0, 1).getValues()[0];
    this.data = this.range.offset(1, 0, this.range.getNumRows() - 1, this.range.getNumColumns());
    this.values = this.data.getValues();
  }

  findColumnIndex(columnName) {
    return this.headers.findIndex(header => header.toString().trim().toLowerCase() === columnName.toLowerCase());
  }

  updateColumnData(columnIndex, newData) {
    for (let i = 0; i < newData.length; i++) {
      this.values[i][columnIndex] = newData[i];
    }
    this.data.setValues(this.values);
  }
}

class DropdownManager {
  constructor(sheetHelper, topicsIndex) {
    this.sheetHelper = sheetHelper;
    this.topicsIndex = topicsIndex;
    this.allowedMap = {};
  }

  extractAllowedOptions(sampleCell) {
    const rule = sampleCell.getDataValidation();
    if (!rule) return;

    const criteria = rule.getCriteriaType();
    const criteriaValues = rule.getCriteriaValues();
    let allowedOptions = [];

    if (criteria === SpreadsheetApp.DataValidationCriteria.VALUE_IN_LIST) {
      if (typeof criteriaValues[0] === 'string') {
        try {
          allowedOptions = this.sheetHelper.sheet.getRange(criteriaValues[0]).getValues().flat().map(val => val.toString().trim());
        } catch (e) {
          this.sheetHelper.showAlert("Error", "Error processing dropdown range.");
          return;
        }
      } else if (Array.isArray(criteriaValues[0])) {
        allowedOptions = criteriaValues[0].map(val => val.toString().trim());
      }
    }

    allowedOptions.forEach(option => this.allowedMap[option.toLowerCase()] = option);
  }
}

class TopicUpdater {
  constructor(tableProcessor, topicsIndex, topicIndex, allowedMap) {
    this.tableProcessor = tableProcessor;
    this.topicsIndex = topicsIndex;
    this.topicIndex = topicIndex;
    this.allowedMap = allowedMap;
  }

  processTopics() {
    const updatedTopics = this.tableProcessor.values.map(row => {
      const topicCellVal = row[this.topicIndex];
      if (!topicCellVal) return row[this.topicsIndex];

      const topicsToAdd = TopicUpdater.parseTopicCell(topicCellVal.toString());
      if (!topicsToAdd.length) return row[this.topicsIndex];

      let existingTopics = (row[this.topicsIndex] || "").split(",").map(t => t.trim()).filter(t => t);
      let existingTopicsLower = new Set(existingTopics.map(t => t.toLowerCase()));
      
      topicsToAdd.forEach(rawTopic => {
        let lowerTopic = rawTopic.trim().toLowerCase();
        let finalTopic = this.allowedMap[lowerTopic] || rawTopic.trim();
        if (!existingTopicsLower.has(finalTopic.toLowerCase())) {
          existingTopics.push(finalTopic);
        }
      });

      return existingTopics.join(", ");
    });

    this.tableProcessor.updateColumnData(this.topicsIndex, updatedTopics);
  }

  static parseTopicCell(cellText) {
    cellText = cellText.trim();
    if (cellText.startsWith("[") && cellText.endsWith("]")) {
      try {
        return JSON.parse(cellText.replace(/'/g, '"')).map(t => t.trim());
      } catch {
        return cellText.slice(1, -1).split(",").map(t => t.trim());
      }
    }
    return cellText.split(",").map(t => t.trim());
  }
}

function dropdownGenerator() {
  const sheetHelper = SpreadsheetHelper.getActiveSheet();
  const sheetRange = sheetHelper.sheet.getRange("B3").getValue().toString();
  
  const confirmResponse = sheetHelper.ui.alert("Confirm Data Location", `Sheet: '${sheetHelper.sheet.getName()}' Range: '${sheetRange}'`, sheetHelper.ui.ButtonSet.YES_NO_CANCEL);
  if (confirmResponse === sheetHelper.ui.Button.NO || confirmResponse === sheetHelper.ui.Button.CANCEL) return;

  const tableProcessor = new TableProcessor(sheetHelper, sheetRange);
  const topicsIndex = tableProcessor.findColumnIndex("Topics");
  const topicIndex = tableProcessor.findColumnIndex("Topic");
  if (topicsIndex === -1 || topicIndex === -1) {
    sheetHelper.showAlert("Error", "Could not find both 'Topics' and 'Topic' columns.");
    return;
  }

  const dropdownManager = new DropdownManager(sheetHelper, topicsIndex);
  dropdownManager.extractAllowedOptions(sheetHelper.sheet.getRange(tableProcessor.range.getRow() + 1, tableProcessor.range.getColumn() + topicsIndex));

  const topicUpdater = new TopicUpdater(tableProcessor, topicsIndex, topicIndex, dropdownManager.allowedMap);
  topicUpdater.processTopics();
  
  sheetHelper.showAlert("Success", "Topics have been merged successfully!");
}
