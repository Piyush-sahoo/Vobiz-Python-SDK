# Vobiz XML Status

*Last updated: 2026-03-19*

---

## Overview

The XML layer is now fully aligned with the official Vobiz specification.

Key changes:

* `Gather` is the **only input collection verb**
* Legacy elements `GetInput` and `GetDigits` have been **removed**
* `AudioStream` is now **implemented and supported**
* Validation has been **standardized and enforced**

  * `Dial` requires nested `Number` or `User`
  * `Record` requires `action`

All XML tests are passing:

* `tests/xml → 46 passed`

---

## Root + Supported Verbs

The root `Response` supports the following child elements:

* Conference
* Dial
* DTMF
* AudioStream
* Gather
* Hangup
* Message
* Play
* PreAnswer
* Record
* Redirect
* Speak
* Wait
* MultiPartyCall
* Stream

Defined in: `vobiz/xml/ResponseElement.py`

---

## Element Status

| Element        | Status | Notes                                                               |
| -------------- | ------ | ------------------------------------------------------------------- |
| Response       | ✅      | Root element, no attributes                                         |
| Speak          | ✅      | Supports SSML-style nesting                                         |
| Play           | ✅      | Supports `loop`                                                     |
| Dial           | ✅      | Fully implemented; enforces `Number`/`User`; `confirmTimeout` fixed |
| Number         | ✅      | Supports digit sending options                                      |
| User           | ✅      | Supports SIP headers and digit sending                              |
| Gather         | ✅      | Single unified input verb (DTMF + speech)                           |
| Record         | ✅      | Requires `action`; supports callbacks and transcription             |
| Hangup         | ✅      | Supports `reason`, `schedule`                                       |
| Redirect       | ✅      | URL + method                                                        |
| Wait           | ✅      | Timing + silence controls                                           |
| Conference     | ✅      | Fully supported                                                     |
| DTMF           | ✅      | Supports async sending                                              |
| PreAnswer      | ✅      | Strict nesting: `Speak`, `Play`, `Wait`                             |
| Stream         | ✅     | XML supported; runtime handling out of scope                        |
| MultiPartyCall | ✅      | Fully supported                                                     |
| Message        | ✅      | Messaging support                                                   |
| AudioStream    | ✅      | Implemented and exposed via builder                                 |

---

## Gather Behavior

`Gather` is the single, spec-compliant input verb.

### Key Rules

* `action` is **required** (must be a valid URL)
* Supports:

  * `dtmf`
  * `speech`
  * `dtmf speech`

### Supported Attributes

* method (`GET` / `POST`)
* executionTimeout
* digitEndTimeout
* speechEndTimeout
* finishOnKey
* numDigits
* speechModel
* hints (validated)
* language (allowlisted)
* interimSpeechResultsCallback (+ method)
* log
* redirect
* profanityFilter

### Nesting

* Speak
* Play

Defined in: `vobiz/xml/gatherElement.py`

---

## Breaking Changes

This refactor introduces **intentional breaking changes**:

* Removed:

  * `GetInputElement`
  * `GetDigitsElement`
* Removed builder methods:

  * `add_get_input`
  * `add_get_digits`
* `Record` now requires `action`
* `Dial` now enforces at least one nested `Number` or `User`

These changes ensure strict spec compliance and prevent invalid XML generation.

---

## Validation Guarantees

The XML builder now enforces correctness at construction time:

* Required attributes must be provided
* Invalid configurations raise clear exceptions
* Non-spec elements are not allowed

This reduces runtime failures caused by malformed XML.

---

## Test Coverage

XML layer coverage includes:

* All core verbs
* Validation rules
* Builder wiring

Latest result:

* `pytest tests/xml -q`
* **46 passed**

---

## Usage Guidelines

* Use `Gather` for all input flows (DTMF, speech, or both)
* Do not use legacy input verbs (removed)
* Use `AudioStream` when required by your flow
* Treat `Stream` as XML-only; implement runtime handling separately

---

## Scope Notes

This SDK provides **XML construction only**.

The following are intentionally out of scope:

* Call execution engine
* Webhook orchestration
* Redirect flow control
* Stream WebSocket runtime handling

These are handled by the Vobiz platform.
